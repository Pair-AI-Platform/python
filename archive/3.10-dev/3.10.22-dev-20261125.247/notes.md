## `ghcr.io/pair-ai-platform/python:3.10.22-dev-20261125.247`

Python 3.10.22 (dev). Index digest `sha256:43734a993f080158c12f5ef1ede054c4e38ef4d5ffa131d63c18b4db7691ed89`.
Tags: `3.10.22-dev-20261125.247`, `3.10-dev`, `3.10.22-dev`.

### What changed

No package changed; the image metadata did.

### SBOM and size

| Architecture | Packages (SBOM) | Compressed | Installed |
| :--- | :--- | :--- | :--- |
| x86_64 | 81 | 292.8 MB | 292.8 MB |
| aarch64 | 81 | 276.2 MB | 799.5 MB |

Main components: `binutils 2.47-r4`, `ca-certificates-bundle 20261020-r1`, `gcc 16.2.0-r5`, `git 2.56.1-r2`, `glibc-2.44 2.44-r26`, `glibc-2.44-dev 2.44-r26`, `glibc-2.44-iconv-common 2.44-r26`, `libffi 3.8.1-r0`, `libffi-dev 3.8.1-r0`, `libstdc++ 16.2.0-r5`, `libstdc++-dev 16.2.0-r5`, `make 4.4.1-r16`, `openssl-3.6-libcrypto 3.6.5-r7`, `openssl-3.6-libssl 3.6.5-r7`, `openssl-4.0-dev 4.0.3-r8`, `openssl-4.0-libcrypto 4.0.3-r8`, `openssl-4.0-libssl 4.0.3-r8`, `py3-pip-wheel 26.3-r0`, `python-3.10-upstream 3.10.22-r0`, `python-3.10-upstream-dev 3.10.22-r0`, `python-3.13-base 3.13.18_git20261122-r0`, `sqlite-libs 3.54.1-r1`.
The SPDX SBOMs are attached to this release and to each image as signed attestations.

### Scans

| Architecture | Hardening profile, DISA GPOS SRG (applicable rules passed) | Not applicable | Vulnerabilities (C / H / M / L) |
| :--- | :--- | :--- | :--- |
| x86_64 | 85 / 91 (93.4%) | 107 | 0 / 0 / 3 / 1 |
| aarch64 | 85 / 91 (93.4%) | 107 | 0 / 0 / 3 / 1 |

### Vulnerabilities

| ID | Severity | Package | Installed | Comes from | Fixed upstream in | Architectures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [CVE-2026-115819](https://nvd.nist.gov/vuln/detail/CVE-2026-115819) | Medium | `glibc-2.44` | 2.44-r26 | `glibc-2.44 2.44-r26` | no fix yet | x86_64, aarch64 |
| [CVE-2026-121758](https://nvd.nist.gov/vuln/detail/CVE-2026-121758) | Medium | `glibc-2.44` | 2.44-r26 | `glibc-2.44 2.44-r26` | no fix yet | x86_64, aarch64 |
| [CVE-2026-124024](https://nvd.nist.gov/vuln/detail/CVE-2026-124024) | Medium | `glibc-2.44` | 2.44-r26 | `glibc-2.44 2.44-r26` | no fix yet | x86_64, aarch64 |
| [CVE-2026-100290](https://nvd.nist.gov/vuln/detail/CVE-2026-100290) | Low | `glibc-2.44` | 2.44-r26 | `glibc-2.44 2.44-r26` | no fix yet | x86_64, aarch64 |

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
cosign verify ghcr.io/pair-ai-platform/python:3.10.22-dev-20261125.247 \
  --certificate-identity-regexp '^https://github.com/Pair-AI-Platform/python/.github/workflows/build.yml@' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
gh attestation verify oci://ghcr.io/pair-ai-platform/python:3.10.22-dev-20261125.247 --repo Pair-AI-Platform/python
```
