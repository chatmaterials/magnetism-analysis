#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def analyze_path(path: Path) -> dict[str, object]:
    outcar = path / "OUTCAR" if path.is_dir() else path
    text = outcar.read_text(errors="ignore")
    energy_match = re.findall(r"TOTEN\s*=\s*([\-0-9.Ee+]+)", text)
    total_match = re.search(r"magnetization\s+([\-0-9.Ee+]+)\s*$", text, re.MULTILINE)
    total_moment = float(total_match.group(1)) if total_match else None
    local_moments = []
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip().lower().startswith("magnetization (x)"):
            for candidate in lines[idx + 1 :]:
                parts = candidate.split()
                if len(parts) < 5:
                    if local_moments:
                        break
                    continue
                if not parts[0].isdigit():
                    if local_moments:
                        break
                    continue
                local_moments.append({"ion": int(parts[0]), "moment": float(parts[4])})
            break
    return {
        "path": str(path),
        "final_energy_eV": float(energy_match[-1]) if energy_match else None,
        "total_moment_muB": total_moment,
        "local_moments": local_moments,
        "observations": ["Magnetic-state summary extracted from OUTCAR-like data."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a magnetic-state calculation.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze_path(Path(args.path).expanduser().resolve())
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
