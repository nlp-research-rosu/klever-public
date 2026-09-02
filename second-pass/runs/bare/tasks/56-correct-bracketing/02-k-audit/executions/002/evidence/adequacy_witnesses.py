#!/usr/bin/env python3
"""Ground witnesses for every claim precondition and its claimed result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


def bracket_seq_spec(text: str, initial_depth: int) -> bool:
    depth = initial_depth
    for character in text:
        if character == "<":
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def main() -> None:
    canonical = load_entry(Path("/reference/canonical.py"), "witness_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/proof/solution.py"), "witness_generated"
    )
    witnesses = [
        {
            "claim": "loop-zero",
            "precondition": "none; D is exactly 0",
            "BS": "<>",
            "D": 0,
            "processed_prefix": "",
        },
        {
            "claim": "loop-positive",
            "precondition": "D > 0",
            "BS": ">",
            "D": 1,
            "processed_prefix": "<",
        },
        {
            "claim": "universal-correctness",
            "precondition": "none",
            "BS": "<<>>",
            "D": 0,
            "processed_prefix": "",
        },
    ]
    mismatch_count = 0
    for witness in witnesses:
        remaining = str(witness["BS"])
        depth = int(witness["D"])
        full_input = str(witness["processed_prefix"]) + remaining
        claimed = bracket_seq_spec(remaining, depth)
        expected = canonical(full_input)
        actual = generated(full_input)
        ok = claimed == expected == actual
        print(
            f"WITNESS claim={witness['claim']} "
            f"precondition={witness['precondition']!r} "
            f"BS={remaining!r} D={depth} full_input={full_input!r} "
            f"claimed={claimed} canonical={expected} generated={actual} match={ok}"
        )
        mismatch_count += int(not ok)

    examples = [
        ("example-single-open", "<", False),
        ("example-pair", "<>", True),
        ("example-nested", "<<><>>", True),
        ("example-negative-prefix", "><<>", False),
    ]
    for claim, text, claimed in examples:
        expected = canonical(text)
        actual = generated(text)
        ok = claimed == expected == actual
        print(
            f"WITNESS claim={claim} precondition='none' input={text!r} "
            f"claimed={claimed} canonical={expected} generated={actual} match={ok}"
        )
        mismatch_count += int(not ok)
    print(f"WITNESS_MISMATCHES count={mismatch_count}")
    if mismatch_count:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
