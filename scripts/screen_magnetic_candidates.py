#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from compare_magnetic_states import compare


def analyze_candidate(root: Path, target_ground_state: str, target_moment_min: float) -> dict[str, object]:
    states = sorted(path for path in root.iterdir() if path.is_dir())
    if not states:
        raise SystemExit(f"No magnetic states found in {root}")
    compared = compare(states)
    results = compared["results"]
    ground = results[0] if results else None
    if ground is None:
        raise SystemExit(f"No magnetic results were parsed in {root}")
    moment = abs(float(ground["total_moment_muB"])) if ground["total_moment_muB"] is not None else 0.0
    ordering_penalty = 0.0 if target_ground_state == "any" or ground["magnetic_character"].startswith(target_ground_state) else 25.0
    moment_penalty = max(0.0, target_moment_min - moment)
    split = float(compared["energy_window_meV"]) if compared["energy_window_meV"] is not None else 0.0
    robustness_penalty = max(0.0, 10.0 - split)
    compensation = ground.get("moment_compensation_ratio")
    compensation_penalty = 0.0
    if target_ground_state == "ferromagnetic-like" and compensation is not None:
        compensation_penalty = max(0.0, 0.7 - float(compensation)) * 10.0
    score = ordering_penalty + moment_penalty + robustness_penalty + compensation_penalty
    return {
        "case": root.name,
        "path": str(root),
        "ground_state_character": ground["magnetic_character"],
        "ground_state_path": ground["path"],
        "ground_state_total_moment_muB": ground["total_moment_muB"],
        "energy_window_meV": compared["energy_window_meV"],
        "exchange_proxy_meV_per_active_site": compared["exchange_proxy_meV_per_active_site"],
        "robustness_class": compared["robustness_class"],
        "ordering_penalty": ordering_penalty,
        "moment_penalty": moment_penalty,
        "robustness_penalty": robustness_penalty,
        "compensation_penalty": compensation_penalty,
        "screening_score": score,
    }


def analyze_candidates(roots: list[Path], target_ground_state: str, target_moment_min: float) -> dict[str, object]:
    cases = [analyze_candidate(root, target_ground_state, target_moment_min) for root in roots]
    ranked = sorted(cases, key=lambda item: item["screening_score"])
    return {
        "target_ground_state": target_ground_state,
        "target_moment_min_muB": target_moment_min,
        "ranking_basis": "screening_score = ordering_penalty + moment_penalty + robustness_penalty + compensation_penalty",
        "cases": ranked,
        "best_case": ranked[0]["case"] if ranked else None,
        "observations": [
            "This is a compact magnetic-screening heuristic intended for ranking candidate orderings, not a full spin-model fit."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank magnetic candidates with a simple ground-state screening heuristic.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--target-ground-state", choices=["ferromagnetic-like", "antiferromagnetic-like", "ferrimagnetic-like", "any"], default="ferromagnetic-like")
    parser.add_argument("--target-moment-min", type=float, default=1.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze_candidates(
        [Path(path).expanduser().resolve() for path in args.paths],
        args.target_ground_state,
        args.target_moment_min,
    )
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
