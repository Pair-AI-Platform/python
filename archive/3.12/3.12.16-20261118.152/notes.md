## `ghcr.io/pair-ai-platform/python:3.12.16-20261118.152`

Python 3.12.16 (runtime). Index digest `sha256:401028e14bdb22e4cbfaa95b1f1179fba3c9d45aa9acab213e769fe0f4ca6dc5`.
Tags: `3.12.16-20261118.152`, `3.12`, `3.12.16`, `latest`.

### What changed

| Package | From | To |
| :--- | :--- | :--- |
| `mpdecimal` | 4.0.1-r6 | 4.0.1-r7 |

### SBOM and size

| Architecture | Packages (SBOM) | Compressed | Installed |
| :--- | :--- | :--- | :--- |
| x86_64 | 37 | 43.4 MB | 43.5 MB |
| aarch64 | 37 | 41.6 MB | 119.0 MB |

Main components: `ca-certificates-bundle 20261020-r0`, `glibc-2.44 2.44-r23`, `libffi 3.8.1-r0`, `libstdc++ 16.2.0-r5`, `openssl-4.0-libcrypto 4.0.3-r8`, `openssl-4.0-libssl 4.0.3-r8`, `py3-pip-wheel 26.2.2-r3`, `python-3.12 3.12.16_git20261116-r0`, `python-3.12-base 3.12.16_git20261116-r0`, `python-3.13-base 3.13.18_git20261115-r1`, `sqlite-libs 3.54.1-r1`.
The SPDX SBOMs are attached to this release and to each image as signed attestations.

### Scans

| Architecture | Hardening profile, DISA GPOS SRG (applicable rules passed) | Not applicable | Vulnerabilities (C / H / M / L) |
| :--- | :--- | :--- | :--- |
| x86_64 | 85 / 91 (93.4%) | 107 | 0 / 0 / 4 / 1 |
| aarch64 | 85 / 91 (93.4%) | 107 | 0 / 0 / 4 / 1 |

### Vulnerabilities

| ID | Severity | Package | Installed | Comes from | Fixed upstream in | Architectures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [CVE-2026-115559](https://nvd.nist.gov/vuln/detail/CVE-2026-115559) | Medium | `python-3.12` | 3.12.16_git20261116-r0 | `python-3.12 3.12.16_git20261116-r0` | no fix yet | x86_64, aarch64 |
| [CVE-2026-115791](https://nvd.nist.gov/vuln/detail/CVE-2026-115791) | Medium | `python-3.12` | 3.12.16_git20261116-r0 | `python-3.12 3.12.16_git20261116-r0` | no fix yet | x86_64, aarch64 |
| [CVE-2026-116566](https://nvd.nist.gov/vuln/detail/CVE-2026-116566) | Medium | `python-3.12` | 3.12.16_git20261116-r0 | `python-3.12 3.12.16_git20261116-r0` | no fix yet | x86_64, aarch64 |
| [CVE-2026-124249](https://nvd.nist.gov/vuln/detail/CVE-2026-124249) | Medium | `python-3.12` | 3.12.16_git20261116-r0 | `python-3.12 3.12.16_git20261116-r0` | no fix yet | x86_64, aarch64 |
| [CVE-2026-103995](https://nvd.nist.gov/vuln/detail/CVE-2026-103995) | Low | `python-3.12` | 3.12.16_git20261116-r0 | `python-3.12 3.12.16_git20261116-r0` | no fix yet | x86_64, aarch64 |
| [CVE-2026-19552](https://nvd.nist.gov/vuln/detail/CVE-2026-19552) | Negligible | `python-3.12` | 3.12.16_git20261116-r0 | `python-3.12 3.12.16_git20261116-r0` | no fix yet | x86_64, aarch64 |

*Comes from* is the Wolfi package that brings the affected code into the image; a library bundled inside the toolchain, for example, comes from that package. *Fixed upstream in* is the version of the affected code that fixes it; the image gets the fix when the package it comes from ships that version, and the next build after that publishes it.

Hardening-profile rules not passed (x86_64):

- `SV-203649r971535_rule`: The operating system must use mechanisms meeting the requirements of applicable federal laws, Executive orders, directives, policies, regulations, standards, and guidance for authentication to a cryptographic module.
- `SV-203739r987791_rule`: The operating system must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.
- `SV-203750r958912_rule`: The operating system must maintain the confidentiality and integrity of information during preparation for transmission.
- `SV-203751r958914_rule`: The operating system must maintain the confidentiality and integrity of information during reception.
- `SV-203776r959006_rule`: The operating system must implement NIST FIPS-validated cryptography for the following: to provision digital signatures, to generate cryptographic hashes, and to protect unclassified information requiring confidentiality and cryptographic protection in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.
- `SV-263659r982563_rule`: The operating system must include only approved trust anchors in trust stores or certificate stores managed by the organization.

### Verify

```sh
cosign verify ghcr.io/pair-ai-platform/python:3.12.16-20261118.152 \
  --certificate-identity-regexp '^https://github.com/Pair-AI-Platform/python/.github/workflows/build.yml@' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
gh attestation verify oci://ghcr.io/pair-ai-platform/python:3.12.16-20261118.152 --repo Pair-AI-Platform/python
```
