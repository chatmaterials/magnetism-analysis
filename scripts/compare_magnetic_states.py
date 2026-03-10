#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyze_magnetic_state import analyze_path


def compare(paths: list[Path]) -> dict[str, object]:
    records = [analyze_path(path) for path in paths]
    energies = [record["final_energy_eV"] for record in records if record["final_energy_eV"] is not None]
    reference = min(energies) if energies else None
    for record in records:
        energy = record["final_energy_eV"]
        record["relative_energy_meV"] = (energy - reference) * 1000.0 if energy is not None and reference is not None else None
    records.sort(key=lambda item: (item["final_energy_eV"] is None, item["final_energy_eV"]))
    lowest = records[0] if records else None
    second = records[1] if len(records) > 1 else None
    gap = None
    if lowest is not None and second is not None and lowest["relative_energy_meV"] is not None and second["relative_energy_meV"] is not None:
        gap = second["relative_energy_meV"] - lowest["relative_energy_meV"]
    return {
        "reference_energy_eV": reference,
        "ground_state_path": lowest["path"] if lowest is not None else None,
        "ground_state_character": lowest["magnetic_character"] if lowest is not None else None,
        "energy_window_meV": gap,
        "results": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare multiple magnetic-state calculations.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = compare([Path(path).expanduser().resolve() for path in args.paths])
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
