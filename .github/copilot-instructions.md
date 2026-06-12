# Copilot instructions for this repository

## Project shape

This repository is a small Windows-oriented Python CLI that generates an RTSDK Java `pom.xml`.
The entry point is `maven_pom_generator.py`, which loads RTSDK version data from `config/rtsdk_versions.yaml` and renders `templates/rtsdk_maven_pom_xml.txt` with Jinja2 into `output/pom.xml`.

## Run commands

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python maven_pom_generator.py --api EMA --version 2.4.0 --jdkversion 17
python maven_pom_generator.py --help
```

Use `--api EMA|ETA`, `--version <RTSDK version>`, and `--jdkversion <supported JDK>`.
The default output path is `output\pom.xml`.

## Architecture

- `config/rtsdk_versions.yaml` is the source of truth for RTSDK-to-Maven version mapping, supported JDKs, JavaFX versions, and shared namespace/transport values.
- `maven_pom_generator.py` is a thin CLI wrapper:
  - reads YAML config
  - validates CLI choices against supported JDKs and API values
  - computes a small `sdk_information` context dict
  - renders the Jinja2 template
  - writes the generated pom to `output/pom.xml`
- `templates/rtsdk_maven_pom_xml.txt` contains the generated Maven structure, including API-specific dependencies and the main class for the assembly plugin.

## Conventions

- Keep generation logic in the template/config split: add or tweak version mappings in YAML first; only change Python when the CLI flow or context assembly changes.
- Preserve the API-specific behavior:
  - EMA uses `com.refinitiv.ema`, JavaFX dependencies, and test-scoped JUnit.
  - ETA uses `com.refinitiv.eta.*`, Mockito, and compile-scoped JUnit.
- When adding new RTSDK releases, update `rtsdk_versions`, `latest_version`, `support_jdk_versions`, and `javafx_versions` together so the CLI choices stay consistent.
- The generated artifact ID is derived from the API and resolved RTSDK version, so changes to version resolution affect output naming.
- The repository ignores `venv/` and `output/`; generated files should stay out of source control.
