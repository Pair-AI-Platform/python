#!/usr/bin/env bash
# Scans one single-platform image with OpenSCAP against the STIG profile in the Wolfi package
# chainguard-security-guide (based on the DISA General Purpose Operating System SRG), and writes
# the results.
#
#   scripts/stig-scan.sh <image-ref> <out-dir>
#
# <image-ref> must be available to the local Docker daemon (pulled or loaded). Writes
# <out-dir>/results.xml (XCCDF results), <out-dir>/report.html and <out-dir>/summary.json with the
# counts per result and the score: pass / (pass + fail), so rules that are not applicable to a
# container (no kernel, no SSH, no login) do not count either way.
#
# The root filesystem is extracted as root inside the scanner, so file ownership is kept (several
# rules check for root:root).
#
# Known limit: SV-263659 (approved trust anchors) also checks that SSL_CERT_FILE is set in the
# environment of the running processes. A filesystem scan has no processes, so OpenSCAP reports that
# rule as failed even though the image sets SSL_CERT_FILE. The CA bundle part of the rule (bundle
# present and matching its checksum stamp) is checked by the image tests instead.
set -euo pipefail

image="$1"
out="$(mkdir -p "$2" && cd "$2" && pwd)"

# The scanner image built from scanner/stig-scanner.apko.yaml (Wolfi packages openscap and
# chainguard-security-guide); see the README for building it locally
OPENSCAP_IMAGE="${OPENSCAP_IMAGE:-stig-scanner:local}"
DATASTREAM=/usr/share/xml/scap/ssg/content/ssg-chainguard-gpos-ds.xml
PROFILE=xccdf_basic_profile_.check

cid="$(docker create "$image" true 2>/dev/null || docker create "$image")"
trap 'docker rm "$cid" >/dev/null 2>&1 || true' EXIT

chmod 777 "$out"
docker export "$cid" | docker run --rm -i -u 0 -v "$out:/out" \
  --entrypoint sh "$OPENSCAP_IMAGE" -c "
    mkdir /rootfs && tar -x -C /rootfs
    oscap-chroot /rootfs xccdf eval --profile '$PROFILE' \
      --results /out/results.xml --report /out/report.html '$DATASTREAM' > /out/oscap.log 2>&1
    # oscap exits 2 when any rule fails; that is a result, not an error
    rc=\$?; [ \$rc -eq 0 ] || [ \$rc -eq 2 ]
    chmod a+r /out/*"

python3 - "$out/results.xml" "$out/summary.json" <<'EOF'
import json, sys, xml.etree.ElementTree as ET
ns = {"x": "http://checklists.nist.gov/xccdf/1.2"}
root = ET.parse(sys.argv[1]).getroot()
titles = {r.get("id"): " ".join((r.findtext("x:title", "", ns) or "").split()) for r in root.iter("{%s}Rule" % ns["x"])}
counts, failed = {}, []
for rr in root.iter("{%s}rule-result" % ns["x"]):
    result = rr.findtext("x:result", "", ns)
    counts[result] = counts.get(result, 0) + 1
    if result in ("fail", "error"):
        rule = rr.get("idref")
        failed.append({"rule": rule.split("_rule_")[-1], "title": titles.get(rule, ""), "result": result})
applicable = counts.get("pass", 0) + counts.get("fail", 0)
summary = {
    "profile": "chainguard-security-guide ssg-chainguard-gpos-ds.xml (DISA GPOS SRG), xccdf_basic_profile_.check",
    "counts": counts,
    "applicable": applicable,
    "score": round(100 * counts.get("pass", 0) / applicable, 1) if applicable else None,
    "failed": sorted(failed, key=lambda f: f["rule"]),
}
json.dump(summary, open(sys.argv[2], "w"), indent=2)
print(json.dumps({k: summary[k] for k in ("counts", "applicable", "score")}))
EOF
