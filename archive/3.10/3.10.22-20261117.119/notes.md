## `ghcr.io/pair-ai-platform/python:3.10.22-20261117.119`

Python 3.10.22 (runtime). Index digest `sha256:3654b764d38afc2641cfd50fc02c05c57a00dbc42bc6a9e4d46cea8b4e6418af`.
Tags: `3.10.22-20261117.119`, `3.10`, `3.10.22`.

### What changed

| Package | From | To |
| :--- | :--- | :--- |
| `glibc-2.44` | 2.44-r20 | 2.44-r21 |
| `glibc-2.44-locale-posix` | 2.44-r20 | 2.44-r21 |
| `ld-linux-2.44` | 2.44-r20 | 2.44-r21 |
| `libcrypt1-2.44` | 2.44-r20 | 2.44-r21 |

### SBOM and size

| Architecture | Packages (SBOM) | Compressed | Installed |
| :--- | :--- | :--- | :--- |
| x86_64 | 38 | 55.2 MB | 55.2 MB |
| aarch64 | 38 | 52.2 MB | 138.5 MB |

Main components: `ca-certificates-bundle 20261020-r0`, `glibc-2.44 2.44-r21`, `libffi 3.8.1-r0`, `libstdc++ 16.2.0-r4`, `openssl-3.6-libcrypto 3.6.5-r6`, `openssl-3.6-libssl 3.6.5-r6`, `openssl-4.0-libcrypto 4.0.3-r8`, `openssl-4.0-libssl 4.0.3-r8`, `py3-pip-wheel 26.2.2-r3`, `python-3.10-upstream 3.10.22-r0`, `python-3.13-base 3.13.18_git20261115-r1`, `sqlite-libs 3.54.1-r0`.
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
cosign verify ghcr.io/pair-ai-platform/python:3.10.22-20261117.119 \
  --certificate-identity-regexp '^https://github.com/Pair-AI-Platform/python/.github/workflows/build.yml@' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
gh attestation verify oci://ghcr.io/pair-ai-platform/python:3.10.22-20261117.119 --repo Pair-AI-Platform/python
```
