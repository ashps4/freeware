# PS4 GhidraOrbis AIO — R6 eboot analysis

This repository runs a static analysis of the public `eboot.bin` attached to:

- Repository: `ashps4/freeware`
- Release tag: `R6`
- Asset filename match: `eboot.bin`

It is designed to be launched from a phone through the GitHub Actions web UI.

## What the workflow does

1. Downloads Ghidra 12.1.4 and uses Java 21.
2. Checks out GhidraOrbis tag `1.0156`, builds the extension with Gradle 8.14, and installs it into the Ghidra distribution.
3. Downloads `eboot.bin` from the public `R6` release (or uses `game/eboot.bin` when supplied in this repository).
4. Prints the file size, SHA-256, first 64 bytes, and a cautious ELF/SELF format hint.
5. Runs Ghidra headless analysis with a larger Java heap and a five-hour per-file analysis timeout.
6. Exports discovered functions to CSV and HTML, and uploads logs and reports as an Actions artifact.

GhidraOrbis is built from its upstream source at tag `1.0156`. Its upstream repository documents support for Ghidra 10.0+ and its build workflow includes Ghidra 12.1.4. Ghidra 12.2 is not selected here because the upstream build matrix shown for this integration does not list 12.2. Pinning 12.1.4 avoids an unverified API combination.

## Start from a phone

1. Upload the contents of this ZIP into the root of your GitHub repository, preserving `.github/workflows/ghidra.yml`.
2. Commit the files to the repository's default branch (usually `main`).
3. Open **Actions**.
4. Select **PS4 GhidraOrbis R6 analysis**.
5. Tap **Run workflow**.
6. When it finishes, download the artifact **PS4-GhidraOrbis-R6-Analysis**.
7. Open `reports/index.html` or `reports/all_functions.csv`. For diagnostics, open `logs/eboot.log`, `loader-diagnostics.txt`, and `eboot-inspection.txt`.

The workflow is manual (`workflow_dispatch`) so it will not automatically consume Actions minutes on each push.

## About the eboot file and decryption

Putting a file in the GitHub runner, downloading it, extracting it, or importing it into Ghidra does not decrypt it. A PS4 game executable may be a SELF container. Retail NPDRM SELF files are normally protected at rest. OpenOrbis can create fake SELF (`fSELF`) outputs; the workflow prints a header hint so we can tell whether the file looks consistent with that format. The hint is not a cryptographic proof.

GhidraOrbis provides Orbis/PS4 file-format and analysis support; it is not a retail SELF decryption tool and does not supply Sony decryption keys. If `eboot.bin` is a retail encrypted SELF, a separate legally authorized plaintext ELF or memory image is required for meaningful code analysis. This workflow deliberately does not attempt to bypass console security or decrypt retail executables.

## Memory and timeout settings

The workflow sets `GHIDRA_HEADLESS_MAXMEM` to 8 GB on larger runners or 5 GB on smaller runners. Ghidra's headless launcher supports this environment variable. The analysis timeout is 18,000 seconds (five hours); `0` is intentionally not used because it caused an immediate timeout in the earlier run.

## Expected output

- `reports/eboot.functions.csv` — functions recognized by Ghidra
- `reports/all_functions.csv` — merged CSV
- `reports/index.html` — browser-friendly function table
- `logs/eboot.log` — Ghidra analysis log
- `logs/ghidraorbis-build.log` — extension build log
- `loader-diagnostics.txt` — loader/language messages extracted from Ghidra's log
- `eboot-inspection.txt` — file header, SHA-256 and format hint
- `build/` — built GhidraOrbis extension archive

A successful GitHub Actions status alone does not prove that functions were found; check the CSV row count and loader diagnostics.

## License and upstream components

- Ghidra: Apache License 2.0, from the National Security Agency's public repository.
- GhidraOrbis: GPL-3.0, built from the upstream repository during the workflow.
- This AIO workflow and its helper scripts are provided as integration glue; upstream licenses remain applicable to their respective components.
