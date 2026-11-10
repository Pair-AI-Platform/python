# Where Python comes from

| Image | Python package | Source | Verification |
| :--- | :--- | :--- | :--- |
| `python:3.13`, `python:3.13-dev` | `python-3.13` | Wolfi (`packages.wolfi.dev`) | Wolfi repository APK signature |
| `python:3.12` (`latest`), `python:3.12-dev` (`latest-dev`) | `python-3.12` | Wolfi (`packages.wolfi.dev`) | Wolfi repository APK signature |
| `python:3.11`, `python:3.11-dev` | `python-3.11-upstream` | Official source from [python.org](https://www.python.org/ftp/python/), compiled here with Melange | OpenPGP signature (`.asc`) from Pablo Galindo Salgado (`64E628F8D684696D`) |
| `python:3.10`, `python:3.10-dev` | `python-3.10-upstream` | Official source from [python.org](https://www.python.org/ftp/python/), compiled here with Melange | OpenPGP signature (`.asc`) from Pablo Galindo Salgado (`64E628F8D684696D`) |

---

## Why Python 3.10 and 3.11 come from python.org

Wolfi and Chainguard move non-latest and older LTS releases from the public Wolfi repository (`packages.wolfi.dev`) to Chainguard's commercial enterprise repository. Once a Python branch leaves the public repository, public packages freeze and no longer receive security fixes or patch updates without a paid commercial license.

To guarantee continuous, unblocked security updates and long-term reproducibility without vendor lock-in, all Python LTS versions that are restricted, frozen, or commercial-only in Wolfi are compiled directly from the official source published by the Python Software Foundation (PSF) on [python.org](https://www.python.org/downloads/).

---

## How upstream packages are built and verified

Each Melange recipe (e.g. [`melange/python-3.10-upstream.yaml`](../melange/python-3.10-upstream.yaml), [`melange/python-3.11-upstream.yaml`](../melange/python-3.11-upstream.yaml)) runs natively on `x86_64` and `aarch64`:

1. **Download:** Fetches `Python-<version>.tar.xz` and its detached OpenPGP signature `Python-<version>.tar.xz.asc` from `https://www.python.org/ftp/python/<version>/`.
2. **Cryptographic Verification:** Verifies the archive with `gpgv` against the official Python Release Manager keys ([`python-release-keys.kbx`](../melange/python-3.10-upstream/python-release-keys.kbx)):
   - **Thomas Wouters** (`7169605F62C751356D054A26A821E680E5FA6305`, Key ID `A821E680E5FA6305`) for Python 3.12 and 3.13.
   - **Pablo Galindo Salgado** (`A035C8C19219BA821ECEA86B64E628F8D684696D`, Key ID `64E628F8D684696D`) for Python 3.10 and 3.11.
   The build halts immediately if the signature is missing or fails verification.
3. **Hardened Compilation:** Builds Python from source with production-grade flags:
   ```sh
   ./configure \
     --prefix=/usr \
     --enable-shared \
     --with-system-expat \
     --with-system-ffi \
     --without-ensurepip \
     --enable-loadable-sqlite-extensions \
     --with-lto \
     --enable-optimizations
   make -j"$(nproc)"
   make DESTDIR="${{targets.destdir}}" install
   ```
4. **Footprint Optimization:** Removes internal test directories (`test/`, `tests/`) and bytecode files (`.pyc`) to minimize the image footprint and attack surface.
5. **Split Development Headers:** Uses Melange's `split/dev` to package development headers and pkg-config files into `-dev` subpackages (`python-3.10-upstream-dev`).
6. **Package Signing:** Signs the resulting `.apk` packages using the repository's dedicated RSA key (`keys/python-packages.rsa.pub`).

---

## How Renovate keeps them current

[Renovate](../renovate.json) continuously monitors upstream Python releases and automates security patches:

| What | Renovate datasource | Rule |
| :--- | :--- | :--- |
| Python 3.13 | `python-version` / `github-releases` | Newest `3.13.x` release from python.org; automerged once images build, test and scan |
| Python 3.12 | `python-version` / `github-releases` | Newest `3.12.x` release from python.org; automerged once images build, test and scan |
| Python 3.11 | `python-version` / `github-releases` | Newest `3.11.x` release from python.org; automerged once images build, test and scan |
| Python 3.10 | `python-version` / `github-releases` | Newest `3.10.x` release from python.org; automerged once images build, test and scan |
| Release keys | `scripts/update-python-release-keys.sh` | Refreshes release manager keyring if signing keys or subkeys rotate |

When python.org issues a new release (including critical CVE fixes), Renovate opens a pull request. Once all CI checks pass (Melange compilation, image integration tests, OpenSCAP STIG audit, Grype vulnerability scan), the pull request is squashed and merged automatically, triggering release publication to GHCR with Sigstore signatures and SLSA L3 provenance.

---

## If Wolfi moves another line

`python-3.12` and `python-3.13` are currently in public Wolfi. If either line is moved to Chainguard's commercial repository in the future:
1. Ready-to-use upstream recipes [`melange/python-3.12-upstream.yaml`](../melange/python-3.12-upstream.yaml) and [`melange/python-3.13-upstream.yaml`](../melange/python-3.13-upstream.yaml) are already maintained in the repository.
2. In `apko/python-3.12.apko.yaml`, simply update the package name from `python-3.12` to `python-3.12-upstream`.
3. `scripts/plan.py` automatically detects the change, marks the image as local, and builds it from official python.org sources without modifying CI pipelines.
