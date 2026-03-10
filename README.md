# magnetism-analysis

[![CI](https://img.shields.io/github/actions/workflow/status/chatmaterials/magnetism-analysis/ci.yml?branch=main&label=CI)](https://github.com/chatmaterials/magnetism-analysis/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/chatmaterials/magnetism-analysis?display_name=tag)](https://github.com/chatmaterials/magnetism-analysis/releases)

Standalone skill for magnetism-focused DFT result analysis.

## Install

```bash
npx skills add chatmaterials/magnetism-analysis -g -y
```

## Local Validation

```bash
python3 -m py_compile scripts/*.py
npx skills add . --list
python3 scripts/analyze_magnetic_state.py fixtures/fm --json
python3 scripts/compare_magnetic_states.py fixtures/compare/fm fixtures/compare/afm --json
python3 scripts/export_magnetism_report.py fixtures/compare/fm fixtures/compare/afm
python3 scripts/run_regression.py
```
