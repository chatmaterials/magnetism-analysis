#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from compare_magnetic_states import compare


def screening_note(payload: dict[str, object]) -> str:
    ground_state = payload.get("ground_state_character")
    window = payload.get("energy_window_meV")
    if ground_state is None:
        return "No ground-state classification could be inferred from the supplied paths."
    if window is None:
        return f"The lowest-energy state looks `{ground_state}`, but there is no second state to assess energetic robustness."
    if float(window) < 5.0:
        return f"The lowest-energy state looks `{ground_state}`, but the magnetic energy splitting is small enough that competing orderings may remain close."
    exchange_proxy = payload.get("exchange_proxy_meV_per_active_site")
    if exchange_proxy is not None:
        return f"The lowest-energy state looks `{ground_state}` with a `{payload.get('robustness_class')}` magnetic splitting of about `{float(window):.2f}` meV, or `{float(exchange_proxy):.2f}` meV per active local moment."
    return f"The lowest-energy state looks `{ground_state}` with a magnetic splitting of about `{float(window):.2f}` meV to the next state."


def render_markdown(payload: dict[str, object]) -> str:
    lines = ["# Magnetism Analysis Report", ""]
    for record in payload["results"]:
        lines.extend(
            [
                f"## {Path(record['path']).name}",
                f"- Final energy (eV): `{record['final_energy_eV']:.6f}`",
                f"- Relative energy (meV): `{record['relative_energy_meV']:.4f}`" if record["relative_energy_meV"] is not None else "- Relative energy (meV): `unknown`",
                f"- Total moment (muB): `{record['total_moment_muB']:.4f}`" if record["total_moment_muB"] is not None else "- Total moment (muB): `unknown`",
                f"- Magnetic character: `{record['magnetic_character']}`",
                f"- Max local moment (muB): `{record['max_local_moment_muB']:.4f}`" if record["max_local_moment_muB"] is not None else "- Max local moment (muB): `n/a`",
                f"- Local moment RMS (muB): `{record['local_moment_rms_muB']:.4f}`" if record["local_moment_rms_muB"] is not None else "- Local moment RMS (muB): `n/a`",
                "",
            ]
        )
    lines.extend(["## Screening Note", f"- {screening_note(payload)}", ""])
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
