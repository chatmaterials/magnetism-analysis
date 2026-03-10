---
name: "magnetism-analysis"
description: "Use when the task is to analyze magnetic DFT results, including total and local magnetic moments, comparing ferromagnetic and antiferromagnetic states, ranking magnetic configurations by energy, and writing compact markdown reports from finished calculations."
---

# Magnetism Analysis

Use this skill for magnetism-focused post-processing rather than generic workflow setup.

## When to use

- extract total or local magnetic moments from finished calculations
- compare FM and AFM states by energy
- summarize magnetic-state ordering or energy splitting
- write a compact magnetism-analysis report from finished calculations

## Use the bundled helpers

- `scripts/analyze_magnetic_state.py`
  Summarize a single magnetic-state calculation.
- `scripts/compare_magnetic_states.py`
  Compare multiple magnetic-state calculations by energy and total moment.
- `scripts/export_magnetism_report.py`
  Export a markdown magnetism-analysis report.

## Guardrails

- Do not interpret simple total-energy differences as a full magnetic model by themselves.
- Distinguish local-moment extraction from exchange-parameter fitting.
