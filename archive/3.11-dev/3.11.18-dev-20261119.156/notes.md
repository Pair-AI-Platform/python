## `ghcr.io/pair-ai-platform/python:3.11.18-dev-20261119.156`

Python 3.11.18 (dev). Index digest `sha256:7e52a0ff34c1ab014a27a19a964d17b8dd35a1b7d347477bc376da2a22494b54`.
Tags: `3.11.18-dev-20261119.156`, `3.11-dev`, `3.11.18-dev`.

### What changed

| Package | From | To |
| :--- | :--- | :--- |
| `libbrotlicommon1` | 1.2.1-r3 | 1.2.1-r4 |
| `libbrotlidec1` | 1.2.1-r3 | 1.2.1-r4 |
| `libbrotlienc1` | 1.2.1-r3 | 1.2.1-r4 |
| `libnghttp2-14` | 1.71.0-r0 | 1.71.0-r1 |
| `nghttp3` | 1.19.0-r0 | 1.19.0-r1 |
| `ngtcp2` | 1.26.0-r0 | 1.26.0-r1 |

### SBOM and size

| Architecture | Packages (SBOM) | Compressed | Installed |
| :--- | :--- | :--- | :--- |
| x86_64 | 80 | 305.8 MB | 305.8 MB |
| aarch64 | 80 | 288.8 MB | 831.7 MB |

Main components: `binutils 2.47-r4`, `ca-certificates-bundle 20261020-r0`, `gcc 16.2.0-r5`, `git 2.56.1-r1`, `glibc-2.44 2.44-r23`, `glibc-2.44-dev 2.44-r23`, `libffi 3.8.1-r0`, `libffi-dev 3.8.1-r0`, `libstdc++ 16.2.0-r5`, `libstdc++-dev 16.2.0-r5`, `make 4.4.1-r16`, `openssl-3.6-libcrypto 3.6.5-r6`, `openssl-3.6-libssl 3.6.5-r6`, `openssl-4.0-dev 4.0.3-r8`, `openssl-4.0-libcrypto 4.0.3-r8`, `openssl-4.0-libssl 4.0.3-r8`, `py3-pip-wheel 26.2.2-r3`, `python-3.11-upstream 3.11.18-r0`, `python-3.11-upstream-dev 3.11.18-r0`, `python-3.13-base 3.13.18_git20261115-r1`, `sqlite-libs 3.54.1-r1`.
The SPDX SBOMs are attached to this release and to each image as signed attestations.

### Scans

| Architecture | Hardening profile, DISA GPOS SRG (applicable rules passed) | Not applicable | Vulnerabilities (C / H / M / L) |
| :--- | :--- | :--- | :--- |
| x86_64 | 85 / 91 (93.4%) | 107 | 0 / 0 / 0 / 0 |
| aarch64 | 85 / 91 (93.4%) | 107 | 0 / 0 / 0 / 0 |

### Vulnerabilities

None found.

Hardening-profile rules not passed (x86_64):

- `SV-203649r971535_rule`: The operating system must use mechanisms meeting the requirements of applicable federal laws, Executive orders, directives, policies, regulations, standards, and guidance for authentication to a cryptographic module.
- `SV-203739r987791_rule`: The operating system must implement NSA-approved cryptography to protect classified information in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.
- `SV-203750r958912_rule`: The operating system must maintain the confidentiality and integrity of information during preparation for transmission.
- `SV-203751r958914_rule`: The operating system must maintain the confidentiality and integrity of information during reception.
- `SV-203776r959006_rule`: The operating system must implement NIST FIPS-validated cryptography for the following: to provision digital signatures, to generate cryptographic hashes, and to protect unclassified information requiring confidentiality and cryptographic protection in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards.
- `SV-263659r982563_rule`: The operating system must include only approved trust anchors in trust stores or certificate stores managed by the organization.

### Verify

```sh
cosign verify ghcr.io/pair-ai-platform/python:3.11.18-dev-20261119.156 \
  --certificate-identity-regexp '^https://github.com/Pair-AI-Platform/python/.github/workflows/build.yml@' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
gh attestation verify oci://ghcr.io/pair-ai-platform/python:3.11.18-dev-20261119.156 --repo Pair-AI-Platform/python
```
