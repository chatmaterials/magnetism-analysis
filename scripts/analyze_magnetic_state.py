#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from magnetism_io import analyze_state


def analyze_path(path: Path) -> dict[str, object]:
    payload = analyze_state(Path(path).expanduser().resolve())
    payload["observations"] = [
        f"Magnetic-state summary extracted from {payload['backend']}-style data.",
        f"Magnetic character was classified as `{payload['magnetic_character']}`.",
    ]
    return payload


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
