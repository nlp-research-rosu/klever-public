#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential for HumanEval 157."""

from __future__ import annotations

import importlib.util
import itertools
import json
import pathlib
import random
import sys
from collections.abc import Callable, Iterable
from typing import Any


def load_entry(path: pathlib.Path, module_name: str) -> Callable[..., Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "right_angle_triangle")
    if not callable(entry):
        raise TypeError(f"entry point in {path} is not callable")
    return entry


def outcome(function: Callable[..., Any], args: list[Any] | tuple[Any, ...]) -> Any:
    try:
        value = function(*args)
    except Exception as error:  # compare observable exception classes
        return {"exception": type(error).__name__}
    return {"value": value, "type": type(value).__name__}


def compare_cases(
    label: str,
    cases: Iterable[list[Any] | tuple[Any, ...]],
    canonical: Callable[..., Any],
    candidate: Callable[..., Any],
) -> tuple[int, int, list[dict[str, Any]]]:
    total = 0
    mismatches = 0
    examples: list[dict[str, Any]] = []
    for args in cases:
        total += 1
        canonical_outcome = outcome(canonical, args)
        candidate_outcome = outcome(candidate, args)
        if canonical_outcome != candidate_outcome:
            mismatches += 1
            if len(examples) < 20:
                examples.append(
                    {
                        "args": list(args),
                        "canonical": canonical_outcome,
                        "candidate": candidate_outcome,
                    }
                )
    print(
        json.dumps(
            {
                "scope": label,
                "cases": total,
                "mismatches": mismatches,
                "mismatch_examples": examples,
            },
            sort_keys=True,
        )
    )
    return total, mismatches, examples


def main() -> int:
    if len(sys.argv) != 4:
        print(
            f"usage: {sys.argv[0]} INPUTS.json CANONICAL.py CANDIDATE.py",
            file=sys.stderr,
        )
        return 64

    inputs_path = pathlib.Path(sys.argv[1])
    canonical_path = pathlib.Path(sys.argv[2])
    candidate_path = pathlib.Path(sys.argv[3])
    with inputs_path.open("r", encoding="utf-8") as stream:
        inputs = json.load(stream)

    canonical = load_entry(canonical_path, "audit_trusted_canonical")
    candidate = load_entry(candidate_path, "audit_candidate_solution")

    compare_cases(
        "documented_examples",
        inputs["documented_examples"],
        canonical,
        candidate,
    )
    compare_cases(
        "branch_and_boundary_cases",
        inputs["branch_and_boundary_cases"],
        canonical,
        candidate,
    )
    _, arity_mismatches, _ = compare_cases(
        "empty_and_arity_cases",
        inputs["arity_cases"],
        canonical,
        candidate,
    )

    cube = inputs["generated_integer_cube"]
    cube_range = range(cube["minimum"], cube["maximum"] + 1)
    cube_cases = itertools.product(cube_range, repeat=3)
    _, broad_cube_mismatches, _ = compare_cases(
        "exhaustive_integer_cube",
        cube_cases,
        canonical,
        candidate,
    )

    positive_range = range(max(1, cube["minimum"]), cube["maximum"] + 1)
    _, positive_mismatches, _ = compare_cases(
        "exhaustive_positive_length_cube",
        itertools.product(positive_range, repeat=3),
        canonical,
        candidate,
    )

    generated = inputs["generated_random_integers"]
    rng = random.Random(generated["seed"])
    random_cases = [
        [
            rng.randint(generated["minimum"], generated["maximum"]),
            rng.randint(generated["minimum"], generated["maximum"]),
            rng.randint(generated["minimum"], generated["maximum"]),
        ]
        for _ in range(generated["count"])
    ]
    _, random_mismatches, _ = compare_cases(
        "seeded_broad_integer_sample",
        random_cases,
        canonical,
        candidate,
    )

    print(
        json.dumps(
            {
                "summary": {
                    "arity_mismatches": arity_mismatches,
                    "broad_cube_mismatches": broad_cube_mismatches,
                    "positive_length_mismatches": positive_mismatches,
                    "random_broad_mismatches": random_mismatches,
                },
                "interpretation": (
                    "Broad-domain differences are recorded evidence, not ignored. "
                    "Success means the harness ran and positive-length results plus "
                    "arity behavior matched."
                ),
            },
            sort_keys=True,
        )
    )
    return 0 if positive_mismatches == 0 and arity_mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
