#!/usr/bin/env bash
# Scans one single-platform image for known vulnerabilities with Grype.
#
#   scripts/vuln-scan.sh <image-ref> <out-dir>
#
# <image-ref> must be available to the local Docker daemon. Writes <out-dir>/grype.json and
# <out-dir>/summary.json with the number of findings per severity, how many of them already have a
# fixed version in Wolfi (those disappear with the next rebuild), and every finding: the CVE or
# advisory ID with its link, its severity, the affected package and version, the version upstream
# fixed it in, and the Wolfi package it comes from: a library bundled inside npm, for example, is
# fixed in the image only when that npm package is updated.
set -euo pipefail

image="$1"
out="$(mkdir -p "$2" && cd "$2" && pwd)"

# Pinned by digest; Renovate updates it (renovate.json)
GRYPE_IMAGE="${GRYPE_IMAGE:-anchore/grype:v0.121.3@sha256:13113eeceab017260370cf540e1d25442c59665fd07d1b09b66d63bb0c282887}"

docker run --rm -v /var/run/docker.sock:/var/run/docker.sock "$GRYPE_IMAGE" \
  "docker:$image" -o json -q > "$out/grype.json"

# The image's apk database: which installed package owns which file
cid="$(docker create "$image" true 2>/dev/null || docker create "$image")"
docker cp "$cid:/usr/lib/apk/db/installed" - | tar -xO > "$out/apk-installed"
docker rm "$cid" >/dev/null

python3 - "$out/grype.json" "$out/summary.json" "$out/apk-installed" <<'PY'
import json, sys
matches = json.load(open(sys.argv[1]))["matches"]

owner = {}
for entry in open(sys.argv[3]).read().split("\n\n"):
    name = version = directory = ""
    for line in entry.splitlines():
        key, _, value = line.partition(":")
        if key == "P":
            name = value
        elif key == "V":
            version = value
        elif key == "F":
            directory = value
        elif key == "R":
            owner["/" + directory + "/" + value] = f"{name} {version}"


def source(artifact):
    if artifact.get("type") == "apk":
        return f"{artifact['name']} {artifact['version']}"
    for location in artifact.get("locations", []):
        path = location.get("path", "")
        if path in owner:
            return owner[path]
    return ""
order = ["Critical", "High", "Medium", "Low", "Negligible", "Unknown"]
counts = {s: 0 for s in order}
fixable = {s: 0 for s in order}
for m in matches:
    sev = m["vulnerability"].get("severity", "Unknown")
    counts[sev] = counts.get(sev, 0) + 1
    if m["vulnerability"].get("fix", {}).get("state") == "fixed":
        fixable[sev] = fixable.get(sev, 0) + 1
def advisory_url(v):
    # Neutral, public sources: NVD for CVEs, the GitHub Advisory Database for GHSAs
    vid = v["id"]
    if vid.startswith("CVE-"):
        return f"https://nvd.nist.gov/vuln/detail/{vid}"
    if vid.startswith("GHSA-"):
        return f"https://github.com/advisories/{vid}"
    return v.get("dataSource", "")

findings = []
for m in matches:
    v, a = m["vulnerability"], m["artifact"]
    findings.append({
        "id": v["id"],
        "severity": v.get("severity", "Unknown"),
        "package": a["name"],
        "version": a["version"],
        "fixed_in": v.get("fix", {}).get("versions", []),
        "source": source(a),
        "url": advisory_url(v),
    })
rank = {s: i for i, s in enumerate(order)}
findings.sort(key=lambda f: (rank.get(f["severity"], len(order)), f["id"], f["package"]))
summary = {"scanner": "grype", "total": len(matches), "counts": counts, "fixable": fixable,
           "findings": findings}
json.dump(summary, open(sys.argv[2], "w"), indent=2)
print(json.dumps({k: summary[k] for k in ("total", "counts", "fixable")}))
PY
