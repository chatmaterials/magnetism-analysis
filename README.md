# magnetism-analysis

[![CI](https://img.shields.io/github/actions/workflow/status/chatmaterials/magnetism-analysis/ci.yml?branch=main&label=CI)](https://github.com/chatmaterials/magnetism-analysis/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/chatmaterials/magnetism-analysis?display_name=tag)](https://github.com/chatmaterials/magnetism-analysis/releases)

Standalone skill for magnetism-focused DFT result analysis, including magnetic-state classification, local-moment descriptors, and mode-specific multi-candidate screening.

Supports VASP and QE-style magnetic outputs.

## Install

```bash
npx skills add chatmaterials/magnetism-analysis -g -y
```

## Local Validation

```bash
python3 -m py_compile scripts/*.py
npx skills add . --list
python3 scripts/analyze_magnetic_state.py fixtures/fm --json
python3 scripts/analyze_magnetic_state.py fixtures/ferri --json
python3 scripts/analyze_magnetic_state.py fixtures/qe/fm --json
python3 scripts/compare_magnetic_states.py fixtures/compare/fm fixtures/compare/afm --json
python3 scripts/screen_magnetic_candidates.py fixtures/compare fixtures/candidates/weak-fm fixtures/candidates/ferri-mixed --target-ground-state ferromagnetic-like --target-moment-min 1.5 --mode ordered --json
python3 scripts/screen_magnetic_candidates.py fixtures/compare fixtures/candidates/compensated-robust fixtures/candidates/ferri-mixed --target-ground-state antiferromagnetic-like --target-moment-min 1.0 --mode compensated --json
python3 scripts/screen_magnetic_candidates.py fixtures/candidates/weak-fm fixtures/candidates/ferri-mixed --target-ground-state any --target-moment-min 1.0 --mode local-moment --json
python3 scripts/export_magnetism_report.py fixtures/compare/fm fixtures/compare/afm
python3 scripts/run_regression.py
```
