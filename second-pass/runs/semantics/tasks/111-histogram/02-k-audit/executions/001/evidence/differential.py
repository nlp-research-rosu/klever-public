#!/usr/bin/env python3
"""Independent differential check for HumanEval 111 histogram."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_histogram(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_histogram("trusted_canonical_111", args.canonical)
    generated = load_histogram("candidate_generated_111", args.generated)

    documented = [
        "",
        "a b c",
        "a b b a",
        "a b c a b",
        "b b b b a",
    ]
    branch_boundaries = [
        "a",
        "a a",
        "a b",
        "a a b",
        "a b b",
        "a b a",
        "a b c c",
        "a b c a",
        "a a b b c",
        "a b c d e f g",
        "z z z y y x",
        " ".join(chr(ord("a") + i) for i in range(26)),
        " ".join(["a"] * 1000),
    ]

    # Exhaust every sequence through length 7 over a three-letter alphabet.
    exhaustive = [
        " ".join(tokens)
        for length in range(8)
        for tokens in itertools.product("abc", repeat=length)
    ]

    rng = random.Random(111)
    random_cases = [
        " ".join(rng.choice("abcxyz") for _ in range(rng.randrange(0, 51)))
        for _ in range(500)
    ]

    intended = list(dict.fromkeys(documented + branch_boundaries + exhaustive + random_cases))

    # These diagnose the boundary of the prompt phrase "space separated
    # lowercase letters"; they are not counted as members of the strict
    # intended domain (empty or [a-z]( [a-z])*).
    outside_domain = [
        " ",
        "  ",
        "a ",
        " a",
        "a  b",
        "a   a",
        "a\tb",
        "a\nb",
        "aa bb",
        "A B",
        "a !",
    ]

    intended_mismatches = []
    for value in intended:
        oracle = canonical(value)
        observed = generated(value)
        if observed != oracle:
            intended_mismatches.append(
                {"input": value, "canonical": oracle, "generated": observed}
            )

    boundary_results = []
    for value in outside_domain:
        oracle = canonical(value)
        observed = generated(value)
        boundary_results.append(
            {
                "input": value,
                "canonical": oracle,
                "generated": observed,
                "equal": observed == oracle,
            }
        )

    args.inputs_out.write_text(
        json.dumps(
            {
                "strict_intended_domain": "empty or [a-z]( [a-z])*",
                "documented": documented,
                "branch_boundaries": branch_boundaries,
                "intended_inputs": intended,
                "outside_domain_probes": outside_domain,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"documented_count={len(documented)}")
    print(f"branch_boundary_count={len(branch_boundaries)}")
    print(f"exhaustive_count={len(exhaustive)}")
    print(f"random_count={len(random_cases)} seed=111")
    print(f"deduplicated_intended_count={len(intended)}")
    print(f"intended_mismatch_count={len(intended_mismatches)}")
    if intended_mismatches:
        print(json.dumps(intended_mismatches[:20], indent=2, sort_keys=True))
    print("outside_domain_results=")
    print(json.dumps(boundary_results, indent=2, sort_keys=True))
    return 1 if intended_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
