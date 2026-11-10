#!/usr/bin/env bash
# Refreshes the Python release keyring with the official OpenPGP release manager keys:
# - Thomas Wouters (3.12.x and 3.13.x): key ID A821E680E5FA6305 (7169605F62C751356D054A26A821E680E5FA6305)
# - Pablo Galindo Salgado (3.10.x and 3.11.x): key ID 64E628F8D684696D (A035C8C19219BA821ECEA86B64E628F8D684696D)
# Run when release managers rotate or update subkeys.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

tmpd="$(mktemp -d)"
trap 'rm -rf "$tmpd"' EXIT

echo "Fetching Python release keys from keyserver..."
gpg --homedir "$tmpd" --keyserver hkps://keyserver.ubuntu.com --recv-keys \
  7169605F62C751356D054A26A821E680E5FA6305 \
  A035C8C19219BA821ECEA86B64E628F8D684696D

for recipe_dir in "$ROOT_DIR"/melange/python-*-upstream; do
  if [ -d "$recipe_dir" ]; then
    keyring="$recipe_dir/python-release-keys.kbx"
    cp "$tmpd/pubring.kbx" "$keyring"
    echo "Refreshed keyring at $keyring"
  fi
done
