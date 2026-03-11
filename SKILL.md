---
name: "magnetism-analysis"
description: "Use when the task is to analyze magnetic DFT results, including total and local magnetic moments, magnetic-state classification, local-moment distribution descriptors, comparing ferromagnetic and antiferromagnetic states, mode-specific candidate ranking, and writing compact markdown reports from finished calculations. Supports VASP and QE-style outputs."
---

# Magnetism Analysis

Use this skill for magnetism-focused post-processing rather than generic workflow setup.

## When to use

- extract total or local magnetic moments from finished calculations
- classify magnetic states as nonmagnetic-, ferro-, ferri-, or antiferromagnetic-like
- derive compact local-moment distribution and exchange-scale descriptors
- compare FM and AFM states by energy
- summarize magnetic-state ordering or energy splitting
- rank multiple magnetic candidates in ordered, compensated, or local-moment-focused modes
- write a compact magnetism-analysis report from finished calculations

Supported backends:

- VASP-like `OUTCAR`
- QE-like `pw.x` `.out` files with total magnetization

## Use the bundled helpers

- `scripts/analyze_magnetic_state.py`
  Summarize a single magnetic-state calculation.
- `scripts/compare_magnetic_states.py`
  Compare multiple magnetic-state calculations by energy and total moment.
- `scripts/screen_magnetic_candidates.py`
  Rank multiple magnetic candidates by ground-state character, moment size, and magnetic energy splitting.
- `scripts/export_magnetism_report.py`
  Export a markdown magnetism-analysis report.

## Guardrails

- Do not interpret simple total-energy differences as a full magnetic model by themselves.
- Distinguish local-moment extraction from exchange-parameter fitting.
