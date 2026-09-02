#!/usr/bin/env python3
"""Independent differential test for HumanEval problem 61.

The trusted and generated entry points are imported from paths supplied on the
command line. Inputs are generated here, independently of the K proof helper.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


def all_parenthesis_strings(max_length: int):
    for length in range(max_length + 1):
        for symbols in itertools.product("()", repeat=length):
            yield "".join(symbols)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical")
    parser.add_argument("generated")
    parser.add_argument("inputs_json")
    args = parser.parse_args()

    canonical = load_entry(Path(args.canonical), "trusted_canonical_61")
    generated = load_entry(Path(args.generated), "generated_solution_61")

    documented = ["(", "()", "(()())", ")(()"]
    explicit_boundaries = [
        "",
        ")",
        "((",
        "))",
        "()(",
        "())",
        "(()",
        "()()",
        "((()))",
        "((())())",
        "(((((((((())))))))))",
        "(" * 64 + ")" * 64,
        ")" + "(" * 64 + ")" * 63,
    ]
    exhaustive = list(all_parenthesis_strings(12))
    rng = random.Random(610061)
    generated_cases = [
        "".join(rng.choice("()") for _ in range(length))
        for length in (13, 14, 15, 16, 17, 31, 32, 33, 63, 64, 65, 127, 128)
        for _ in range(32)
    ]

    ordered = []
    seen = set()
    for value in documented + explicit_boundaries + exhaustive + generated_cases:
        if value not in seen:
            seen.add(value)
            ordered.append(value)

    manifest = {
        "domain": "strings containing only '(' and ')'",
        "documented_examples": documented,
        "explicit_boundaries": explicit_boundaries,
        "exhaustive_generation": {
            "alphabet": ["(", ")"],
            "minimum_length": 0,
            "maximum_length": 12,
            "count_before_deduplication": len(exhaustive),
        },
        "deterministic_random_seed": 610061,
        "generated_lengths": [13, 14, 15, 16, 17, 31, 32, 33, 63, 64, 65, 127, 128],
        "generated_per_length": 32,
        "ordered_unique_inputs": ordered,
    }
    Path(args.inputs_json).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    mismatches = []
    for value in ordered:
        expected = canonical(value)
        actual = generated(value)
        if actual != expected:
            mismatches.append(
                {"input": value, "canonical": expected, "generated": actual}
            )

    print(f"documented_examples={len(documented)}")
    print(f"explicit_boundaries={len(explicit_boundaries)}")
    print(f"exhaustive_parenthesis_strings={len(exhaustive)}")
    print(f"deterministic_generated_cases={len(generated_cases)}")
    print(f"ordered_unique_cases={len(ordered)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
