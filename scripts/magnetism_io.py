#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


RY_TO_EV = 13.605693009


def read_text(path: Path) -> str:
    return path.read_text(errors="ignore") if path.exists() else ""


def detect_backend(path: Path) -> str:
    root = path if path.is_dir() else path.parent
    names = {item.name for item in root.iterdir()} if root.is_dir() else set()
    if "OUTCAR" in names:
        return "vasp"
    if any(root.glob("*.out")):
        return "qe"
    raise SystemExit(f"Could not detect magnetic backend from {path}")


def analyze_state(path: Path) -> dict[str, object]:
    backend = detect_backend(path)
    root = path if path.is_dir() else path.parent
    if backend == "vasp":
        text = read_text(root / "OUTCAR")
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
            "backend": backend,
            "path": str(path),
            "final_energy_eV": float(energy_match[-1]) if energy_match else None,
            "total_moment_muB": total_moment,
            "local_moments": local_moments,
        }
    out_files = sorted(root.glob("*.out"))
    if not out_files:
        raise SystemExit(f"No QE output file found in {root}")
    text = read_text(out_files[0])
    energy_match = re.findall(r"!\s+total energy\s+=\s+([\-0-9.DdEe+]+)\s+Ry", text)
    total_match = re.search(r"total magnetization\s*=\s*([\-0-9.Ee+]+)", text, re.IGNORECASE)
    return {
        "backend": backend,
        "path": str(path),
        "final_energy_eV": float(energy_match[-1].replace("D", "e").replace("d", "e")) * RY_TO_EV if energy_match else None,
        "total_moment_muB": float(total_match.group(1)) if total_match else None,
        "local_moments": [],
    }
