## `ghcr.io/pair-ai-platform/python:3.11.18-dev-20261114.62`

Python 3.11.18 (dev). Index digest `sha256:58164d85cd5e969c06d083063421e0e43adb7c8ee0c9a6c01ed68ffab9ce9eb5`.
Tags: `3.11.18-dev-20261114.62`, `3.11-dev`, `3.11.18-dev`.

### What changed

| Package | From | To |
| :--- | :--- | :--- |
| `gmp` | 6.3.0-r12 | 6.3.0-r13 |
| `libcom_err` | 1.47.4-r5 | 1.47.4-r6 |

### SBOM and size

| Architecture | Packages (SBOM) | Compressed | Installed |
| :--- | :--- | :--- | :--- |
| x86_64 | 80 | 305.8 MB | 305.8 MB |
| aarch64 | 80 | 288.8 MB | 831.6 MB |

Main components: `binutils 2.47-r4`, `ca-certificates-bundle 20261020-r0`, `gcc 16.2.0-r3`, `git 2.56.1-r1`, `glibc-2.44 2.44-r19`, `glibc-2.44-dev 2.44-r19`, `libffi 3.8.0-r2`, `libffi-dev 3.8.0-r2`, `libstdc++ 16.2.0-r3`, `libstdc++-dev 16.2.0-r3`, `make 4.4.1-r16`, `openssl-3.6-libcrypto 3.6.5-r6`, `openssl-3.6-libssl 3.6.5-r6`, `openssl-4.0-dev 4.0.3-r8`, `openssl-4.0-libcrypto 4.0.3-r8`, `openssl-4.0-libssl 4.0.3-r8`, `py3-pip-wheel 26.2.2-r2`, `python-3.11-upstream 3.11.18-r0`, `python-3.11-upstream-dev 3.11.18-r0`, `python-3.13-base 3.13.18_git20261030-r0`, `sqlite-libs 3.54.1-r0`.
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
cosign verify ghcr.io/pair-ai-platform/python:3.11.18-dev-20261114.62 \
  --certificate-identity-regexp '^https://github.com/Pair-AI-Platform/python/.github/workflows/build.yml@' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
gh attestation verify oci://ghcr.io/pair-ai-platform/python:3.11.18-dev-20261114.62 --repo Pair-AI-Platform/python
```
