#!/usr/bin/env python3
"""Wrap the trusted-regenerated Program term in concrete run(...) inputs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
program = (ROOT / "regenerated-solution.mpy").read_text().strip()
cases = {
    "3-4-5": (3, 4, 5),
    "1-2-3": (1, 2, 3),
    "5-3-4": (5, 3, 4),
    "3-5-4": (3, 5, 4),
    "0-0-0": (0, 0, 0),
    "0-3-3": (0, 3, 3),
    "3-0-3": (3, 0, 3),
    "3-3-0": (3, 3, 0),
    "neg3-4-5": (-3, 4, 5),
    "3-neg4-5": (3, -4, 5),
    "3-4-neg5": (3, 4, -5),
    "large": (300000000000000000000, 400000000000000000000, 500000000000000000000),
}

for name, values in cases.items():
    rendered_values = ", ".join(str(value) for value in values)
    path = ROOT / f"run-{name}.mpy"
    path.write_text(
        f'run(\n{program},\n"right_angle_triangle",\nArgs({rendered_values}))\n'
    )
    print(f"{path.name}: Args({rendered_values})")
