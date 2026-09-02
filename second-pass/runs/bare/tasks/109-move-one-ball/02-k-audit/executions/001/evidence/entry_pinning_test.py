#!/usr/bin/env python3
"""Check that the claim's `theSolution` executes identically to submitted solution.mpy."""

from __future__ import annotations

from pathlib import Path
import subprocess


DEFINITION = "/tmp/audit-work/build/semantic-llvm-kompiled"
PROGRAMS = [
    Path("/tmp/audit-work/source/solution.mpy"),
    Path("/audit-output/evidence/theSolution.pgm"),
]
INPUTS = [
    ".IList",
    "3 :: 4 :: 5 :: 1 :: 2 :: .IList",
    "2 :: 1 :: 3 :: .IList",
]

for input_term in INPUTS:
    outputs: list[str] = []
    for program in PROGRAMS:
        command = [
            "krun",
            str(program),
            "--definition",
            DEFINITION,
            f"-cINPUT={input_term}",
        ]
        print("$", " ".join(command))
        result = subprocess.run(command, text=True, capture_output=True)
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="")
        print(f"EXIT_STATUS: {result.returncode}")
        if result.returncode != 0:
            raise SystemExit(result.returncode)
        outputs.append(result.stdout)
    same = outputs[0] == outputs[1]
    print(f"PINNING_INPUT={input_term!r} FULL_CONFIGURATION_IDENTICAL={same}")
    if not same:
        raise SystemExit(1)

print(f"PINNING_CASES={len(INPUTS)}")
print("MISMATCH_COUNT=0")

