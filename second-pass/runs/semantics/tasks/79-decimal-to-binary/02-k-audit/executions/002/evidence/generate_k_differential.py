#!/usr/bin/env python3
"""Generate a deterministic concrete K-vs-Python assertion program."""

from __future__ import annotations

import json
import random
from pathlib import Path


def main() -> None:
    rng = random.Random(790079)
    values = (
        list(range(0, 65))
        + [127, 128, 129, 255, 256, 257, 1023, 1024, 1025, 65535]
        + [rng.randrange(0, 10**9) for _ in range(20)]
        + [-1, -2, -15, -32, -103]
    )
    lines = [
        "def decimal_to_binary(decimal):",
        '    return "db" + bin(decimal)[2:] + "db"',
        "",
    ]
    for value in values:
        lines.append(
            f"assert decimal_to_binary({value}) == "
            + repr("db" + bin(value)[2:] + "db")
        )
    program = Path("/tmp/audit-work/task/k_differential.py")
    program.write_text("\n".join(lines) + "\n")
    inputs = Path("/audit-output/evidence/k-differential-inputs.json")
    inputs.write_text(json.dumps({"seed": 790079, "values": values}, indent=2) + "\n")
    print(f"generated_program={program}")
    print(f"generated_inputs={inputs}")
    print(f"case_count={len(values)}")


if __name__ == "__main__":
    main()
