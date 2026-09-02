#!/usr/bin/env python3
"""Wrap the byte-checked submitted MPY program in concrete run terms."""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys


EXPECTED_PROGRAM_SHA256 = (
    "d5ca368d0cd54dd51a7a7b8ea8a62b4ce92b31978b8484435101265b40c7301a"
)


def main() -> int:
    if len(sys.argv) != 4:
        print(
            f"usage: {sys.argv[0]} SOLUTION.mpy CASES.json OUTPUT_DIR",
            file=sys.stderr,
        )
        return 64

    program_path = pathlib.Path(sys.argv[1])
    cases_path = pathlib.Path(sys.argv[2])
    output_dir = pathlib.Path(sys.argv[3])
    program_bytes = program_path.read_bytes()
    actual_hash = hashlib.sha256(program_bytes).hexdigest()
    if actual_hash != EXPECTED_PROGRAM_SHA256:
        raise RuntimeError(
            f"submitted-program hash changed: {actual_hash} "
            f"!= {EXPECTED_PROGRAM_SHA256}"
        )
    program = program_bytes.decode("utf-8").strip()
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)

    for case in cases:
        arguments = ", ".join(str(value) for value in case["args"])
        run_term = (
            "run(\n"
            f"{program},\n"
            '  "right_angle_triangle",\n'
            f"  Args({arguments}))\n"
        )
        destination = output_dir / f"{case['name']}.mpy"
        destination.write_text(run_term, encoding="utf-8")
        print(
            f"{destination} args={case['args']} "
            f"sha256={hashlib.sha256(run_term.encode()).hexdigest()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
