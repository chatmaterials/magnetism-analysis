#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=True)


def run_json(*args: str):
    return json.loads(run(*args).stdout)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    fm = run_json("scripts/analyze_magnetic_state.py", "fixtures/fm", "--json")
    ensure(abs(fm["total_moment_muB"] - 2.4) < 1e-6, "FM fixture should parse the total moment")
    ensure(fm["magnetic_character"] == "ferromagnetic-like", "FM fixture should classify as ferromagnetic-like")
    ensure(fm["active_local_moment_count"] == 2, "FM fixture should count active local moments")
    qe_fm = run_json("scripts/analyze_magnetic_state.py", "fixtures/qe/fm", "--json")
    ensure(abs(qe_fm["total_moment_muB"] - 2.4) < 1e-6, "QE FM fixture should parse the total moment")
    ensure(qe_fm["magnetic_character"] == "polarized-like", "QE FM fixture should classify as polarized-like without local moments")
    ferri = run_json("scripts/analyze_magnetic_state.py", "fixtures/ferri", "--json")
    ensure(ferri["magnetic_character"] == "ferrimagnetic-like", "Ferri fixture should classify as ferrimagnetic-like")
    compare = run_json("scripts/compare_magnetic_states.py", "fixtures/compare/fm", "fixtures/compare/afm", "--json")
    ensure(compare["results"][0]["path"].endswith("fm"), "FM should be lower in energy than AFM in the fixture")
    ensure(compare["results"][1]["relative_energy_meV"] > 0, "AFM should have positive relative energy")
    ensure(compare["ground_state_character"] == "ferromagnetic-like", "The comparison should identify the FM ground state")
    ensure(compare["robustness_class"] == "robust", "The FM/AFM comparison should classify the energy splitting as robust")
    qe_compare = run_json("scripts/compare_magnetic_states.py", "fixtures/qe/compare/fm", "fixtures/qe/compare/afm", "--json")
    ensure(qe_compare["results"][0]["path"].endswith("fm"), "QE FM should be lower in energy than QE AFM in the fixture")
    screened = run_json(
        "scripts/screen_magnetic_candidates.py",
        "fixtures/compare",
        "fixtures/candidates/weak-fm",
        "fixtures/candidates/ferri-mixed",
        "--target-ground-state",
        "ferromagnetic-like",
        "--target-moment-min",
        "1.5",
        "--json",
    )
    ensure(screened["best_case"] == "compare", "magnetism-analysis should rank the robust FM candidate ahead of the weak candidate")
    temp_dir = Path(tempfile.mkdtemp(prefix="magnetism-analysis-report-"))
    try:
        report_path = Path(run("scripts/export_magnetism_report.py", "fixtures/compare/fm", "fixtures/compare/afm", "--output", str(temp_dir / "MAGNETISM_REPORT.md")).stdout.strip())
        report_text = report_path.read_text()
        ensure("# Magnetism Analysis Report" in report_text, "magnetism report should have a heading")
        ensure("Total moment" in report_text, "magnetism report should include the total moment")
        ensure("## Screening Note" in report_text, "magnetism report should include a screening note")
    finally:
        shutil.rmtree(temp_dir)
    print("magnetism-analysis regression passed")


if __name__ == "__main__":
    main()
