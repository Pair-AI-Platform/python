# Python Images on Wolfi

[![SLSA Build L3](https://img.shields.io/badge/SLSA-Build%20L3-orange?style=for-the-badge)](#slsa-build-level-3)
[![Signed with Sigstore](https://img.shields.io/badge/signed-Sigstore%20keyless-purple?style=for-the-badge)](#verify)

Minimal, non-root Python container images for `linux/amd64` and `linux/arm64`, built with
[apko](https://github.com/chainguard-dev/apko) from [Wolfi](https://github.com/wolfi-dev) packages and
verified upstream sources from [python.org](https://www.python.org). Every image is rebuilt every two hours and published again only when its content changed. Every version is:

- **tested** on both architectures with functional, standard library, and C extension compiler checks;
- **scanned** with OpenSCAP against a hardening profile derived from the DISA General Purpose
  Operating System SRG, and for known vulnerabilities with Grype;
- **signed** keyless with Sigstore;
- **attested** with its SBOM, its scan results and SLSA Build Level 3 provenance.

These images ship Python, pip, and standard runtime utilities. Cryptography profiles (for example FIPS 140-3) are
chosen per application and per contract, and are provided separately: see [Cryptography](#cryptography).

## Alignment at a glance

| Area | Aligned with | Evidence in every release |
| :--- | :--- | :--- |
| **Hardening** | OpenSCAP profile derived from the DISA General Purpose Operating System SRG (not an official DISA STIG for containers) | Rules passed out of the applicable ones (about 94% on `python:3.12`), the full report, a signed attestation; see [Security scans](#security-scans) |
| **🇸🇦 Saudi Arabia** | NCA ECC-2:2024 1-6-2-2, 1-6-3-2, 1-6-3-5, 2-1, 2-2-3-3, 2-10-3 · NCA CCC-2:2024 2-3-P-1-3, 2-3-P-1-7, 2-9-T-1-1, 4-1-P-1-2 · NCA CSCC-1:2019 2-3-1-1, 2-3-1-7 · SAMA CSF 3.3.8, 3.3.17 | Minimal non-root baseline, STIG and vulnerability results, SBOM, signatures, provenance |
| **🇰🇼 Kuwait** | CBK CORF 5.3.1.2–5.3.1.5 (hardening against recognized benchmarks), 5.8.1.3 (SBOM), 5.13 (vulnerability and patch management) · NCSC NBCC PR-1, ID-2 | Same, plus rebuilds every two hours |
| **🇦🇪 UAE** | UAE IA Regulation v1.1 T3.2.1, T5.5.4, T7.5.1, T7.7.1, T7.8.1 (superseded by the IA Standard v2.x, 2025; mapping to v2 follows) | Same; the scans use the SCAP formats (XCCDF, OVAL, CVE, CVSS) T7.7 names |
| **🇶🇦 Qatar** | NCSA National Vulnerability Management Guidelines v1.0 (Jan 2026) §6.5 (3–7 days for actively exploited, 14–30 days for CVSS ≥ 7.0), §6.8(b) | Hourly check for fixes, vulnerabilities per release |
| **🇧🇭 Bahrain · 🇴🇲 Oman** | CBB OM-5.5.18, OM-5.5.25, OM-5.5.27, Appendix C · ITA Basic Security Controls 5.5, 5.6, 5.8 | Same |
| **🔐 Cryptography** | FIPS 140-3, CMVP #4985 (security policy §11.1) · 🇸🇦 NCA NCS-1:2020 MODERATE · NCA ECC-2:2024 2-8-3 · NCA DCC-1:2022 2-5-1-2 · SAMA CSF 3.3.9 · 🇰🇼 CBK CORF 5.3.1.3(i), 5.7.1.3, 8.1.4.5 · 🇶🇦 Qatar National Cryptographic Standard v1.0 Tables 1, 2, 4, 5, 7, 10 · 🇦🇪 UAE IA Regulation v1.1 T7.4.1 · 🇧🇭 CBB OM Appendix C (Data Security 1–2) | Compatible with system cryptographic policies or [khatm](https://github.com/Pair-AI-Platform/khatm) when required |

The clause-by-clause table, with links to every document, is in
[Gulf cybersecurity rules at the container level](#gulf-cybersecurity-rules-at-the-container-level).

## Images

`ghcr.io/pair-ai-platform/python:<tag>`. The numbers come from the newest release of each image
and update with every release; click a badge for the details on the image's page:

- **Hardening profile:** rules passed out of the applicable ones, with the full OpenSCAP report.
- **Vulnerabilities:** counts by severity (Critical / High / Medium / Low); the page lists every
  CVE with the affected package and the version that fixes it.
- **SBOM:** packages on amd64 / arm64; the page lists every package with its version and license,
  and links each architecture's SPDX file.
- **Size:** compressed. Each image's [GitHub releases](../../releases) have the same numbers for both
  architectures, plus what changed.

| Image | Python line | Hardening profile (x86_64) | Vulnerabilities | SBOM | Size | Newest release |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `python:3.12` · `latest` | Standard LTS runtime | [![GPOS SRG profile](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.12-stig.json)](https://pair-ai-platform.github.io/python/images/3.12.html#stig) | [![CVEs](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.12-vulns.json)](https://pair-ai-platform.github.io/python/images/3.12.html#vulnerabilities) | [![SBOM](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.12-sbom.json)](https://pair-ai-platform.github.io/python/images/3.12.html#sbom) | ![size](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.12-size.json) | [![release](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.12-release.json)](https://pair-ai-platform.github.io/python/images/3.12.html) |
| `python:3.12-dev` · `latest-dev` | Standard LTS development | [![GPOS SRG profile](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.12-dev-stig.json)](https://pair-ai-platform.github.io/python/images/3.12-dev.html#stig) | [![CVEs](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.12-dev-vulns.json)](https://pair-ai-platform.github.io/python/images/3.12-dev.html#vulnerabilities) | [![SBOM](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.12-dev-sbom.json)](https://pair-ai-platform.github.io/python/images/3.12-dev.html#sbom) | ![size](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.12-dev-size.json) | [![release](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.12-dev-release.json)](https://pair-ai-platform.github.io/python/images/3.12-dev.html) |
| `python:3.13` | Current stable runtime | [![GPOS SRG profile](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.13-stig.json)](https://pair-ai-platform.github.io/python/images/3.13.html#stig) | [![CVEs](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.13-vulns.json)](https://pair-ai-platform.github.io/python/images/3.13.html#vulnerabilities) | [![SBOM](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.13-sbom.json)](https://pair-ai-platform.github.io/python/images/3.13.html#sbom) | ![size](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.13-size.json) | [![release](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.13-release.json)](https://pair-ai-platform.github.io/python/images/3.13.html) |
| `python:3.13-dev` | Current stable development | [![GPOS SRG profile](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.13-dev-stig.json)](https://pair-ai-platform.github.io/python/images/3.13-dev.html#stig) | [![CVEs](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.13-dev-vulns.json)](https://pair-ai-platform.github.io/python/images/3.13-dev.html#vulnerabilities) | [![SBOM](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.13-dev-sbom.json)](https://pair-ai-platform.github.io/python/images/3.13-dev.html#sbom) | ![size](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.13-dev-size.json) | [![release](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.13-dev-release.json)](https://pair-ai-platform.github.io/python/images/3.13-dev.html) |
| `python:3.11` | Maintenance LTS runtime | [![GPOS SRG profile](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.11-stig.json)](https://pair-ai-platform.github.io/python/images/3.11.html#stig) | [![CVEs](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.11-vulns.json)](https://pair-ai-platform.github.io/python/images/3.11.html#vulnerabilities) | [![SBOM](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.11-sbom.json)](https://pair-ai-platform.github.io/python/images/3.11.html#sbom) | ![size](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.11-size.json) | [![release](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.11-release.json)](https://pair-ai-platform.github.io/python/images/3.11.html) |
| `python:3.11-dev` | Maintenance LTS development | [![GPOS SRG profile](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.11-dev-stig.json)](https://pair-ai-platform.github.io/python/images/3.11-dev.html#stig) | [![CVEs](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.11-dev-vulns.json)](https://pair-ai-platform.github.io/python/images/3.11-dev.html#vulnerabilities) | [![SBOM](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.11-dev-sbom.json)](https://pair-ai-platform.github.io/python/images/3.11-dev.html#sbom) | ![size](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.11-dev-size.json) | [![release](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.11-dev-release.json)](https://pair-ai-platform.github.io/python/images/3.11-dev.html) |
| `python:3.10` | Extended maintenance LTS runtime | [![GPOS SRG profile](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.10-stig.json)](https://pair-ai-platform.github.io/python/images/3.10.html#stig) | [![CVEs](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.10-vulns.json)](https://pair-ai-platform.github.io/python/images/3.10.html#vulnerabilities) | [![SBOM](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.10-sbom.json)](https://pair-ai-platform.github.io/python/images/3.10.html#sbom) | ![size](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.10-size.json) | [![release](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.10-release.json)](https://pair-ai-platform.github.io/python/images/3.10.html) |
| `python:3.10-dev` | Extended maintenance LTS dev | [![GPOS SRG profile](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.10-dev-stig.json)](https://pair-ai-platform.github.io/python/images/3.10-dev.html#stig) | [![CVEs](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.10-dev-vulns.json)](https://pair-ai-platform.github.io/python/images/3.10-dev.html#vulnerabilities) | [![SBOM](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.10-dev-sbom.json)](https://pair-ai-platform.github.io/python/images/3.10-dev.html#sbom) | ![size](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.10-dev-size.json) | [![release](https://img.shields.io/endpoint?url=https://pair-ai-platform.github.io/python/badges/3.10-dev-release.json)](https://pair-ai-platform.github.io/python/images/3.10-dev.html) |

Python 3.12 is our default stable LTS line (`latest`), and Python 3.13 is current stable. Python 3.11 and 3.10 are supported extended maintenance LTS lines.
Because Chainguard moved older Python releases to its commercial enterprise repository, public Wolfi packages freeze and no longer receive fixes. We build our Python 3.10 and 3.11 images directly from official python.org source tarballs, cryptographically verified with Python Release Manager OpenPGP keys; see [Where Python comes from](docs/PYTHON-SOURCES.md).

| Flavor | Contents |
| :--- | :--- |
| runtime (`python:3.12`, `python:3.13`, `python:3.11`, `python:3.10`) | Python interpreter, pip, bash, busybox, CA certificates, and time zones. Runs as `nonroot` (1000:1000) in `/app`. Minimal attack surface without C compiler tooling. |
| development (`python:3.12-dev`, etc.) | The standard runtime plus `build-base` (GCC, make, binutils), Python development headers (`python3-dev`), `libffi-dev`, `openssl-dev`, `git`, and `curl` for compiling native Python C extensions (wheels, cython, cffi). |

```dockerfile
# Multi-stage build example
FROM ghcr.io/pair-ai-platform/python:3.12-dev AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Minimal runtime image
FROM ghcr.io/pair-ai-platform/python:3.12
WORKDIR /app
COPY --from=build /install /usr/local
COPY . .
ENTRYPOINT ["/usr/bin/python3", "main.py"]
```

The default entrypoint is `/usr/bin/python3`. Running `docker run ghcr.io/pair-ai-platform/python:3.12 --version`
executes `python3 --version`. For shell interaction, override entrypoint with `--entrypoint bash`.

---

## Tags and versions

| Tag | Example | Moves? |
| :--- | :--- | :--- |
| Release | `3.12.16-20261110.1`, `3.12.16-dev-20261110.1` | Never. One per published version, with its own [GitHub release](../../releases) |
| Patch | `3.12.16`, `3.12.16-dev` | To the newest release of that Python patch release |
| Minor and major | `3.12`, `3.12-dev` | To the newest release of that line |
| `latest`, `latest-dev` | | To the newest release of the default LTS line (3.12) |

Every run takes each image through these steps; a version exists for users only after the last one:

| Step | What happens | If it fails |
| :--- | :--- | :--- |
| 1. Build and test | apko builds the image natively on x86_64 and aarch64 (using locally built Melange packages if applicable); functional, standard library, hardening-profile and vulnerability scans run on each | Nothing is published |
| 2. Compare | Both architectures are built together; each must be byte for byte the image tested in step 1. If the result equals the image under the floating tag (`3.12`), nothing changed and the run stops here for that image | Nothing is published |
| 3. Publish by digest | The image is pushed to GHCR without any tag | Untagged, invisible to users; the cleanup deletes it |
| 4. Sign, attest, verify | Sigstore signatures; SBOM, hardening-profile, vulnerability and SLSA provenance attestations; all verified | Still untagged |
| 5. Tag | The release tag (`3.12.16-20261110.1`) and the floating tags move to the new digest | A re-run of the failed job tags it |
| 6. Release | A GitHub release with the changes, the scan results, the SBOMs and the OpenSCAP report, created only if the tag exists on that digest; the badges are updated | A re-run of the failed job creates it |
| 7. Keep five | The five newest versions of each image stay, in GHCR and as GitHub releases | Never fails a release; runs again next time |

- **Only changed images are published.** The builds are reproducible: the same packages give the
  same digest. An hourly check starts a build as soon as Wolfi ships a new version of something
  inside an image, and the build publishes only the images whose digest changed.
- **Release tags never move and never point to an image without its evidence.** Floating tags
  always point to a kept, signed version.
- **Retention: five versions per image.** GHCR and the GitHub releases keep the five newest versions
  of each image (`3.12`, `3.12-dev`, `3.13`, `3.11`, `3.10`, …).
- **The evidence outlives the image.** For every version ever published, release records, SBOMs and
  OpenSCAP reports are preserved in GitHub Pages archive and Rekor.

---

## Verify

Every published image can be cryptographically verified using `cosign`:

```sh
# Verify signature
cosign verify ghcr.io/pair-ai-platform/python:3.12 \
  --certificate-identity-regexp '^https://github.com/Pair-AI-Platform/python/\.github/workflows/build\.yml@' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com

# Verify SLSA L3 provenance
gh attestation verify oci://ghcr.io/pair-ai-platform/python:3.12 \
  --repo Pair-AI-Platform/python
```

---

## Security scans

Every release publishes its complete scan artifacts and reports:
- **SBOM:** SPDX 2.3 JSON format attached via Cosign attestation and downloadable from GitHub releases.
- **Hardening Profile:** HTML OpenSCAP report published to GitHub Pages and attested via Sigstore predicate.
- **CVE Reports:** Full JSON findings with fixed-in versions and Wolfi source packages.

---

## Gulf cybersecurity rules at the container level

This project aligns base images with the mandatory cybersecurity frameworks of the Gulf Cooperation Council (GCC):

- **Saudi Arabia (NCA):** Essential Cybersecurity Controls (ECC-2:2024), Cloud Cybersecurity Controls (CCC-2:2024), Critical Systems Cybersecurity Controls (CSCC-1:2019), and SAMA Cyber Security Framework.
- **Kuwait (CBK & NCSC):** Cybersecurity Operational Resilience Framework (CORF) and National Baseline Cybersecurity Controls (NBCC).
- **United Arab Emirates (TDRA / DESC):** Information Assurance (IA) Regulation.
- **Qatar (NCSA):** National Vulnerability Management Guidelines and National Cryptographic Standards.
- **Bahrain & Oman:** Central Bank of Bahrain (CBB) Operational Risk Management Regulations and Oman ITA Basic Security Controls.

---

## License

This project is licensed under the [Apache License 2.0](LICENSE). See [NOTICE](NOTICE) for third-party component licenses.

