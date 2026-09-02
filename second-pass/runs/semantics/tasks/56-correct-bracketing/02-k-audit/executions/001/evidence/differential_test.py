#!/usr/bin/env python3
"""Differentially compare trusted canonical.py with the submitted solution."""

from __future__ import annotations

import importlib.util
import hashlib
import itertools
import json
from pathlib import Path
import random


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


def main() -> int:
    canonical = load_entry(
        "trusted_canonical",
        Path("/tmp/audit-work/trusted/canonical.py"),
    )
    submitted = load_entry(
        "submitted_solution",
        Path("/tmp/audit-work/scratch/solution.py"),
    )

    documented = ["<", "<>", "<<><>>", "><<>"]
    boundary = [
        "",
        ">",
        "<<",
        ">>",
        "><",
        "<>",
        "<<>>",
        "<><>",
        "<<>",
        "<>>",
        "<<<>>>",
        "<><<>>",
    ]
    exhaustive = [
        "".join(chars)
        for length in range(13)
        for chars in itertools.product("<>", repeat=length)
    ]

    rng = random.Random(560056)
    generated = []
    for length in (13, 14, 15, 16, 31, 32, 63, 64, 127, 128):
        for _ in range(50):
            generated.append(
                "".join(rng.choice("<>") for _ in range(length))
            )
    generated.extend(["<" * n + ">" * n for n in (1, 2, 16, 64, 256)])
    generated.extend([">" + "<" * n for n in (1, 2, 16, 64, 256)])

    cases = documented + boundary + exhaustive + generated
    input_lines = [
        f"{index}\t{json.dumps(text)}\n"
        for index, text in enumerate(cases)
    ]
    input_blob = "".join(input_lines).encode("utf-8")
    input_path = Path("/audit-output/evidence/differential-inputs.txt")
    input_path.write_bytes(input_blob)

    mismatches = []
    for text in cases:
        expected = canonical(text)
        actual = submitted(text)
        if actual != expected:
            mismatches.append((text, expected, actual))

    print("oracle=/tmp/audit-work/trusted/canonical.py:correct_bracketing")
    print("subject=/tmp/audit-work/scratch/solution.py:correct_bracketing")
    print(f"documented_cases={len(documented)}")
    print(f"explicit_boundary_cases={len(boundary)}")
    print("exhaustive_domain=all '<'/'>' strings of lengths 0..12")
    print(f"exhaustive_cases={len(exhaustive)}")
    print("seed=560056")
    print(
        "random_lengths=13,14,15,16,31,32,63,64,127,128; "
        "50 cases per length"
    )
    print(f"generated_and_long_cases={len(generated)}")
    print(f"total_comparisons={len(cases)}")
    print(f"input_file={input_path}")
    print(f"input_sha256={hashlib.sha256(input_blob).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    for text, expected, actual in mismatches[:20]:
        print(
            f"MISMATCH input={text!r} canonical={expected!r} "
            f"submitted={actual!r}"
        )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
