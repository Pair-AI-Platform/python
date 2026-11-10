#!/usr/bin/env bash
# Functional and hardening checks for one single-platform Python image.
#
#   scripts/test-image.sh <image-ref> <runtime|dev>
set -euo pipefail

image="$1"
flavor="$2"
failed=0

pass() { printf '  ok    %s\n' "$1"; }
fail() { printf '  FAIL  %s\n' "$1"; failed=1; }
check() { local name="$1"; shift; if "$@" >/dev/null 2>&1; then pass "$name"; else fail "$name"; fi; }

pyrun() { docker run --rm -i "$image" "$@"; }
config() { docker image inspect "$image" --format "$1"; }

echo "== $image ($flavor)"

check "python runs" pyrun -c 'import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)'
check "runs as 1000:1000" pyrun -c 'import os; exit(0 if os.getuid() == 1000 and os.getgid() == 1000 else 1)'
check "working directory /app is writable" pyrun -c 'with open("/app/.test_write", "w") as f: f.write("ok"); import os; os.remove("/app/.test_write")'
check "image user is 1000" test "$(config '{{.Config.User}}')" = "1000"
check "SSL_CERT_FILE is set" grep -qx 'SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt' \
  <<<"$(config '{{range .Config.Env}}{{println .}}{{end}}')"

# The CA bundle matches the checksum the ca-certificates package recorded (STIG SV-263659)
check "CA bundle matches its checksum stamp" pyrun -c '
import hashlib
with open("/etc/ssl/certs/.ca-certificates.crt.sha256") as f:
    want = f.read().split()[0]
with open("/etc/ssl/certs/ca-certificates.crt", "rb") as f:
    got = hashlib.sha256(f.read()).hexdigest()
exit(0 if want == got else 1)'

# Shells availability
check "sh is available" docker run --rm --entrypoint sh "$image" -c "exit 0"
check "bash is available" docker run --rm --entrypoint bash "$image" --version

# Python standard library modules validation
check "hashlib and OpenSSL crypto work" pyrun -c 'import hashlib; assert hashlib.sha256(b"pair-ai").hexdigest() == "816d43e5c9bce83e4ba7b11d37b12d1b714b3001850fcbf285f7a0dc08a8a474"'
check "sqlite3 and ctypes work" pyrun -c 'import sqlite3, ctypes; conn = sqlite3.connect(":memory:"); conn.execute("CREATE TABLE t (x);"); conn.close()'
check "compression modules work (zlib, bz2, lzma)" pyrun -c 'import zlib, bz2, lzma; assert zlib.decompress(zlib.compress(b"ok")) == b"ok"'
check "ssl module loads CA certs" pyrun -c 'import ssl; ctx = ssl.create_default_context(); assert ctx.cert_store_stats()["x509"] > 50'

# Pip checks
check "pip is available" docker run --rm --entrypoint pip "$image" --version

if [ "$flavor" = runtime ]; then
  # Runtime image must be minimal: no C compiler installed
  check "no C compiler in runtime" docker run --rm --entrypoint sh "$image" -c '! command -v gcc && ! command -v clang'
else
  # Development image: build tools and C extension compilation
  for tool in gcc make git pkg-config; do
    check "$tool is available" docker run --rm --entrypoint sh "$image" -c "command -v $tool"
  done

  # Test compiling and running a C program using gcc
  check "gcc compiles and links a simple C program" docker run --rm --entrypoint sh "$image" -c '
    cd /app
    cat << "EOF" > test.c
#include <stdio.h>
int main() { printf("pair-ai-python-c-ok\n"); return 0; }
EOF
    gcc test.c -o test_prog
    [ "$(/app/test_prog)" = "pair-ai-python-c-ok" ]
    rm -f test.c test_prog'
fi

if [ "$failed" -ne 0 ]; then
  echo "image checks failed for $image" >&2
  exit 1
fi
echo "all image checks passed"
