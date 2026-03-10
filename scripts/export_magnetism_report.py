#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from compare_magnetic_states import compare


def render_markdown(payload: dict[str, object]) -> str:
    lines = ["# Magnetism Analysis Report", ""]
    for record in payload["results"]:
        lines.extend(
            [
                f"## {Path(record['path']).name}",
                f"- Final energy (eV): `{record['final_energy_eV']:.6f}`",
                f"- Relative energy (meV): `{record['relative_energy_meV']:.4f}`" if record["relative_energy_meV"] is not None else "- Relative energy (meV): `unknown`",
                f"- Total moment (muB): `{record['total_moment_muB']:.4f}`" if record["total_moment_muB"] is not None else "- Total moment (muB): `unknown`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def default_output(source: Path) -> Path:
    return source / "MAGNETISM_REPORT.md" if source.is_dir() else source.parent / "MAGNETISM_REPORT.md"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a markdown magnetism-analysis report.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--output")
    args = parser.parse_args()
    paths = [Path(path).expanduser().resolve() for path in args.paths]
    payload = compare(paths)
    output = Path(args.output).expanduser().resolve() if args.output else default_output(paths[0].parent)
    output.write_text(render_markdown(payload))
    print(output)


if __name__ == "__main__":
    main()
