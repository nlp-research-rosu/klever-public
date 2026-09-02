#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for HumanEval/62."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], list[Any]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.derivative


def stable(value: Any) -> Any:
    if isinstance(value, float):
        return {"float_hex": value.hex()}
    if isinstance(value, list):
        return [stable(item) for item in value]
    return value


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(Path("/candidate/solution.py"), "candidate_generated")

    cases: list[tuple[str, list[Any]]] = [
        ("example-1", [3, 1, 2, 4, 5]),
        ("example-2", [1, 2, 3]),
        ("empty", []),
        ("constant-only", [17]),
        ("first-true-branch", [17, -9]),
        ("zeros", [0, 0, 0, 0]),
        ("negative", [-9, -8, -7, -6]),
        ("large-integers", [10**100, -(10**100), 2**4096, -(2**4096)]),
        ("mixed-floats", [0.5, -1.25, 3.75, -0.0, 1e100]),
        ("booleans", [True, False, True, True]),
        ("sequence-coefficients", ["constant", "a", "bc", ""]),
    ]

    # Exhaust every list through length 5 over a small coefficient alphabet.
    alphabet = [-3, -1, 0, 2, 5]
    for length in range(0, 6):
        for values in itertools.product(alphabet, repeat=length):
            cases.append((f"exhaustive-{length}", list(values)))

    # Deterministic broader generated cases exercise unbounded integers and lengths.
    rng = random.Random(620062)
    for case_number in range(600):
        length = rng.randrange(0, 81)
        values = [rng.randrange(-(10**18), 10**18 + 1) for _ in range(length)]
        cases.append((f"generated-{case_number}", values))

    digest = hashlib.sha256()
    mismatches: list[dict[str, Any]] = []
    for label, original in cases:
        left_input = list(original)
        right_input = list(original)
        try:
            expected = canonical(left_input)
            expected_exc: tuple[str, str] | None = None
        except Exception as err:  # compare behavior as well as values
            expected = None
            expected_exc = (type(err).__name__, str(err))
        try:
            actual = generated(right_input)
            actual_exc: tuple[str, str] | None = None
        except Exception as err:
            actual = None
            actual_exc = (type(err).__name__, str(err))

        record = {
            "label": label,
            "input": stable(original),
            "expected": stable(expected),
            "actual": stable(actual),
            "expected_exception": expected_exc,
            "actual_exception": actual_exc,
            "canonical_mutated_input": left_input != original,
            "candidate_mutated_input": right_input != original,
        }
        digest.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode())
        if (
            expected != actual
            or type(expected) is not type(actual)
            or expected_exc != actual_exc
            or left_input != original
            or right_input != original
        ):
            mismatches.append(record)

    print(f"documented_examples=2")
    print(f"named_boundary_cases=9")
    print(f"exhaustive_small_cases={sum(len(alphabet) ** n for n in range(6))}")
    print("generated_seed=620062 generated_cases=600 generated_lengths=0..80")
    print(f"total_cases={len(cases)}")
    print(f"transcript_sha256={digest.hexdigest()}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print(json.dumps(mismatch, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
