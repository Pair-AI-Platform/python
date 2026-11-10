#!/usr/bin/env python3
"""Release records, notes and status badges for published Python images.

    scripts/release.py record <old-packages.txt> <new-packages.txt> <results-dir>
        Prints the record of one published image as JSON. The package files have one
        "<name> <version>" per line; <results-dir> holds results-<family>-<arch>/ from the test
        job. Reads FAMILY, FLAVOR, IMAGE, INDEX, RELEASE and FLOATING from the environment.

    scripts/release.py notes <record.json>
        Prints the release notes of one image as Markdown.

    scripts/release.py pages <record-dir> <site-dir>
        Writes the status of one image into the GitHub Pages site, from the release record and the
        SBOMs and OpenSCAP reports next to it:
          images/<family>.html          the image page: vulnerabilities, SBOM per architecture, OpenSCAP
          archive/<family>/<release>/   the same evidence for every release, kept after the image is deleted
          sbom/<family>/sbom-<arch>.spdx.json, reports/<family>/stig-<arch>.html
          status/<family>.json and the shields.io endpoint badges
          badges/<family>-{stig,vulns,sbom,size,release}.json
"""
import html
import json
import os
import pathlib
import shutil
import sys

ARCHES = ["x86_64", "aarch64"]
# Shown in the release notes as the main components of each image (name prefixes)
KEY_PREFIXES = ("python-", "py3-", "glibc-", "openssl-", "ca-certificates", "libstdc++", "git", "binutils", "gcc", "make", "sqlite", "libffi")
SEVERITIES = ["Critical", "High", "Medium", "Low", "Negligible", "Unknown"]


def read_packages(path):
    packages = {}
    for line in pathlib.Path(path).read_text().splitlines():
        if line.strip():
            name, version = line.split(" ", 1)
            packages[name] = version
    return packages


def record(old_path, new_path, results):
    old, new = read_packages(old_path), read_packages(new_path)
    family = os.environ["FAMILY"]
    scans = {}
    py_ver = None
    for arch in ARCHES:
        base = pathlib.Path(results) / f"results-{family}-{arch}"
        image = json.loads((base / "image.json").read_text())
        py_ver = py_ver or image.get("python")
        scans[arch] = {
            "digest": image["digest"],
            "sbom": {"packages": image["packages"], "spdx_packages": image["sbom_spdx_packages"]},
            "size": image["size"],
            "stig": json.loads((base / "stig" / "summary.json").read_text()),
            "vulnerabilities": json.loads((base / "vuln" / "summary.json").read_text()),
        }
    return {
        "family": family,
        "flavor": os.environ["FLAVOR"],
        "image": os.environ["IMAGE"],
        "release": os.environ["RELEASE"],
        "floating": os.environ["FLOATING"].split(),
        "digest": os.environ["INDEX"],
        "python": py_ver,
        "first_release": not old,
        "key_packages": [
            f"{n} {new[n]}" for n in sorted(new)
            if n.startswith(KEY_PREFIXES) and not n.endswith(("-locale-posix", "-legacy-allowed"))
        ],
        "packages": {
            "added": sorted(f"{n} {v}" for n, v in new.items() if n not in old),
            "removed": sorted(f"{n} {v}" for n, v in old.items() if n not in new),
            "updated": sorted(
                [n, old[n], new[n]] for n in new if n in old and old[n] != new[n]
            ),
        },
        "scans": scans,
    }


def notes(rec):
    image, release = rec["image"], rec["release"]
    out = [f"## `{image}:{release}`", ""]
    out.append(f"Python {rec['python']} ({rec['flavor']}). Index digest `{rec['digest']}`.")
    out.append("Tags: " + ", ".join(f"`{t}`" for t in [release] + rec["floating"]) + ".")
    out += ["", "### What changed", ""]
    pk = rec["packages"]
    if rec["first_release"]:
        out.append("First release of this image.")
    elif not (pk["added"] or pk["removed"] or pk["updated"]):
        out.append("No package changed; the image metadata did.")
    else:
        out += ["| Package | From | To |", "| :--- | :--- | :--- |"]
        out += [f"| `{n}` | {a} | {b} |" for n, a, b in pk["updated"]]
        out += [f"| `{p.split()[0]}` | (new) | {p.split()[1]} |" for p in pk["added"]]
        out += [f"| `{p.split()[0]}` | {p.split()[1]} | (removed) |" for p in pk["removed"]]
    out += ["", "### SBOM and size", "",
            "| Architecture | Packages (SBOM) | Compressed | Installed |",
            "| :--- | :--- | :--- | :--- |"]
    for arch in ARCHES:
        scan = rec["scans"][arch]
        out.append(f"| {arch} | {scan['sbom']['packages']} | {mb(scan['size']['compressed'])} | {mb(scan['size']['installed'])} |")
    out += ["", "Main components: " + ", ".join(f"`{p}`" for p in rec["key_packages"]) + ".",
            "The SPDX SBOMs are attached to this release and to each image as signed attestations."]
    out += ["", "### Scans", "",
            "| Architecture | Hardening profile, DISA GPOS SRG (applicable rules passed) | Not applicable | Vulnerabilities (C / H / M / L) |",
            "| :--- | :--- | :--- | :--- |"]
    for arch in ARCHES:
        stig = rec["scans"][arch]["stig"]
        vuln = rec["scans"][arch]["vulnerabilities"]["counts"]
        out.append(
            f"| {arch} | {stig['counts'].get('pass', 0)} / {stig['applicable']} ({stig['score']}%) "
            f"| {stig['counts'].get('notapplicable', 0)} "
            f"| {vuln['Critical']} / {vuln['High']} / {vuln['Medium']} / {vuln['Low']} |"
        )
    findings = merged_findings(rec)
    out += ["", "### Vulnerabilities", ""]
    if not findings:
        out.append("None found.")
    else:
        out += ["| ID | Severity | Package | Installed | Comes from | Fixed upstream in | Architectures |",
                "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"]
        out += [f"| [{f['id']}]({f['url']}) | {f['severity']} | `{f['package']}` | {f['version']} "
                f"| `{f.get('source') or f['package']}` | {', '.join(f['fixed_in']) or 'no fix yet'} "
                f"| {', '.join(f['arches'])} |" for f in findings]
        out += ["", FIX_NOTE]
    failed = rec["scans"]["x86_64"]["stig"]["failed"]
    if failed:
        out += ["", "Hardening-profile rules not passed (x86_64):", ""]
        out += [f"- `{f['rule']}`: {f['title']}" for f in failed]
    out += [
        "",
        "### Verify",
        "",
        "```sh",
        f"cosign verify {image}:{release} \\",
        f"  --certificate-identity-regexp '^https://github.com/{os.environ.get('GITHUB_REPOSITORY', '<repo>')}/.github/workflows/build.yml@' \\",
        "  --certificate-oidc-issuer https://token.actions.githubusercontent.com",
        f"gh attestation verify oci://{image}:{release} --repo {os.environ.get('GITHUB_REPOSITORY', '<repo>')}",
        "```",
    ]
    return "\n".join(out) + "\n"


FIX_NOTE = ("*Comes from* is the Wolfi package that brings the affected code into the image; a library "
            "bundled inside the toolchain, for example, comes from that package. *Fixed upstream in* is the "
            "version of the affected code that fixes it; the image gets the fix when the package it comes "
            "from ships that version, and the next build after that publishes it.")


def merged_findings(rec):
    """The vulnerability findings of both architectures, one row per ID and package."""
    merged = {}
    for arch in ARCHES:
        for f in rec["scans"][arch]["vulnerabilities"].get("findings", []):
            key = (f["id"], f["package"], f["version"])
            merged.setdefault(key, {**f, "arches": []})["arches"].append(arch)
    rank = {s: i for i, s in enumerate(SEVERITIES)}
    return sorted(merged.values(), key=lambda f: (rank.get(f["severity"], 99), f["id"], f["package"]))


def sbom_packages(path):
    """The apk packages of an apko SPDX SBOM: name, version and declared license, once each."""
    packages = {}
    for p in json.loads(pathlib.Path(path).read_text()).get("packages", []):
        refs = [r.get("referenceLocator", "") for r in p.get("externalRefs", [])]
        if not any(r.startswith("pkg:apk/") for r in refs):
            continue
        key = (p["name"], p.get("versionInfo", ""))
        license_ = p.get("licenseDeclared") or "NOASSERTION"
        if key not in packages or packages[key] == "NOASSERTION":
            packages[key] = license_
    return [(n, v, l) for (n, v), l in sorted(packages.items())]


def mb(size):
    return f"{size / 1048576:.1f} MB"


def badge(label, message, color):
    return {"schemaVersion": 1, "label": label, "message": message, "color": color}


PAGE_STYLE = """
body{font-family:system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#1f2328}
h1{font-size:1.6rem}h2{margin-top:2rem;border-bottom:1px solid #d0d7de;padding-bottom:.3rem}
table{border-collapse:collapse;width:100%;font-size:.9rem;margin:.5rem 0}
th,td{border:1px solid #d0d7de;padding:.35rem .6rem;text-align:left;vertical-align:top}
th{background:#f6f8fa}code{font-size:.85rem}.Critical,.High{color:#cf222e;font-weight:600}
.Medium{color:#9a6700;font-weight:600}.muted{color:#656d76}
"""


def page(rec, record_dir, site):
    family, e = rec["family"], html.escape
    rows = []
    rows.append(f"<h1>{e(rec['image'])}:{e(rec['release'])}</h1>")
    rows.append(f"<p>Python {e(rec['python'])} ({e(rec['flavor'])}). Tags: "
                + ", ".join(f"<code>{e(t)}</code>" for t in [rec['release']] + rec['floating'])
                + f". Index digest <code>{e(rec['digest'])}</code>.</p>")
    rows.append('<p><a href="#vulnerabilities">Vulnerabilities</a> · <a href="#sbom">SBOM</a> · '
                '<a href="#stig">Hardening profile</a></p>')
    findings = merged_findings(rec)
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITIES}
    rows.append('<h2 id="vulnerabilities">Vulnerabilities</h2>')
    rows.append("<p>" + " · ".join(f"{s}: {n}" for s, n in counts.items() if n) if findings else "<p>None found.")
    rows.append(' <span class="muted">(Grype)</span></p>')
    if findings:
        rows.append("<table><tr><th>ID</th><th>Severity</th><th>Package</th><th>Installed</th>"
                    "<th>Comes from</th><th>Fixed upstream in</th><th>Architectures</th></tr>")
        for f in findings:
            rows.append(f'<tr><td><a href="{e(f["url"])}">{e(f["id"])}</a></td>'
                        f'<td class="{e(f["severity"])}">{e(f["severity"])}</td><td><code>{e(f["package"])}</code></td>'
                        f'<td>{e(f["version"])}</td><td><code>{e(f.get("source") or f["package"])}</code></td>'
                        f'<td>{e(", ".join(f["fixed_in"]) or "no fix yet")}</td>'
                        f'<td>{e(", ".join(f["arches"]))}</td></tr>')
        rows.append("</table>")
        rows.append(f'<p class="muted">{e(FIX_NOTE).replace("*", "")}</p>')
    rows.append('<h2 id="sbom">SBOM</h2><p>One SPDX SBOM per architecture, also attached to the image as a '
                'signed attestation.</p>')
    for arch in ARCHES:
        packages = sbom_packages(pathlib.Path(record_dir) / f"sbom-{arch}.spdx.json")
        size = rec["scans"][arch]["size"]
        rows.append(f'<h3 id="sbom-{arch}">{arch}: {len(packages)} packages</h3>')
        rows.append(f'<p><a href="../sbom/{e(family)}/sbom-{arch}.spdx.json">Download sbom-{arch}.spdx.json</a> · '
                    f'{mb(size["compressed"])} compressed, {mb(size["installed"])} installed</p>')
        rows.append("<table><tr><th>Package</th><th>Version</th><th>License</th></tr>")
        rows += [f"<tr><td><code>{e(n)}</code></td><td>{e(v)}</td><td>{e(l)}</td></tr>" for n, v, l in packages]
        rows.append("</table>")
    rows.append('<h2 id="stig">Hardening profile (OpenSCAP, DISA GPOS SRG)</h2>'
                '<p class="muted">Derived from the DISA General Purpose Operating System SRG; not an official '
                'DISA STIG for containers.</p><table><tr><th>Architecture</th><th>Passed / applicable</th>'
                '<th>Not applicable</th><th>Report</th></tr>')
    for arch in ARCHES:
        st = rec["scans"][arch]["stig"]
        rows.append(f"<tr><td>{arch}</td><td>{st['counts'].get('pass', 0)} / {st['applicable']} ({st['score']}%)</td>"
                    f"<td>{st['counts'].get('notapplicable', 0)}</td>"
                    f'<td><a href="../reports/{e(family)}/stig-{arch}.html">OpenSCAP report</a></td></tr>')
    rows.append("</table>")
    title = f"python:{family}"
    return (f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{e(title)}</title><style>{PAGE_STYLE}</style></head><body>"
            + "\n".join(rows) + "</body></html>\n")


def pages(record_dir, site, archive_release=True):
    record_dir, site = pathlib.Path(record_dir), pathlib.Path(site)
    rec = json.loads((record_dir / "record.json").read_text())
    family = rec["family"]
    for d in ("status", "badges", "images", f"sbom/{family}", f"reports/{family}"):
        (site / d).mkdir(parents=True, exist_ok=True)
    for arch in ARCHES:
        shutil.copy(record_dir / f"sbom-{arch}.spdx.json", site / "sbom" / family / f"sbom-{arch}.spdx.json")
        shutil.copy(record_dir / f"stig-{arch}.html", site / "reports" / family / f"stig-{arch}.html")
    (site / "images" / f"{family}.html").write_text(page(rec, record_dir, site))
    if not archive_release:
        return write_status(rec, site)
    archive = site / "archive" / family / rec["release"]
    archive.mkdir(parents=True, exist_ok=True)
    for f in ["record.json", "notes.md"] + [f"sbom-{a}.spdx.json" for a in ARCHES] + [f"stig-{a}.html" for a in ARCHES]:
        if (record_dir / f).exists():
            shutil.copy(record_dir / f, archive / f)
    (archive / "index.html").write_text(page(rec, record_dir, site).replace(f"../sbom/{family}/", "").replace(
        f"../reports/{family}/", ""))
    write_status(rec, site)


def write_status(rec, site):
    family = rec["family"]
    stig = rec["scans"]["x86_64"]["stig"]
    vulns = {
        s: max(rec["scans"][a]["vulnerabilities"]["counts"].get(s, 0) for a in ARCHES)
        for s in SEVERITIES
    }
    status = {
        "family": family,
        "release": rec["release"],
        "python": rec["python"],
        "digest": rec["digest"],
        "stig": {a: {k: rec["scans"][a]["stig"][k] for k in ("counts", "applicable", "score")} for a in ARCHES},
        "vulnerabilities": {a: rec["scans"][a]["vulnerabilities"]["counts"] for a in ARCHES},
        "sbom": {a: rec["scans"][a]["sbom"] for a in ARCHES},
        "size": {a: rec["scans"][a]["size"] for a in ARCHES},
        "key_packages": rec["key_packages"],
    }
    (site / "status" / f"{family}.json").write_text(json.dumps(status, indent=2) + "\n")
    score = stig["score"]
    color = "brightgreen" if score >= 90 else "yellow" if score >= 75 else "red"
    (site / "badges" / f"{family}-stig.json").write_text(json.dumps(badge(
        "GPOS SRG", f"{stig['counts'].get('pass', 0)}/{stig['applicable']} ({score}%)", color)))
    serious = vulns["Critical"] + vulns["High"]
    color = "brightgreen" if serious == 0 and vulns["Medium"] == 0 else "yellow" if serious == 0 else "red"
    (site / "badges" / f"{family}-vulns.json").write_text(json.dumps(badge(
        "CVEs", f"C{vulns['Critical']} H{vulns['High']} M{vulns['Medium']} L{vulns['Low']}", color)))
    sbom = " / ".join(str(rec["scans"][a]["sbom"]["packages"]) for a in ARCHES)
    (site / "badges" / f"{family}-sbom.json").write_text(json.dumps(badge(
        "SBOM", f"{sbom} packages (amd64 / arm64)", "blue")))
    x86 = rec["scans"]["x86_64"]
    (site / "badges" / f"{family}-size.json").write_text(json.dumps(badge(
        "size", mb(x86["size"]["compressed"]), "blue")))
    (site / "badges" / f"{family}-release.json").write_text(json.dumps(badge(
        "release", rec["release"], "blue")))


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "record":
        print(json.dumps(record(*sys.argv[2:5]), indent=2))
    elif command == "notes":
        print(notes(json.loads(pathlib.Path(sys.argv[2]).read_text())), end="")
    elif command == "pages":
        pages(sys.argv[2], sys.argv[3], archive_release="--no-archive" not in sys.argv[4:])
    else:
        sys.exit(f"unknown command {command}")
