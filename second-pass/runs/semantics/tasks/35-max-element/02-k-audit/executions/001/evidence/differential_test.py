#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py and submitted solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable

CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/35-max-element/solution.py")
INPUT_LOG = Path("/audit-output/evidence/differential-inputs.jsonl")


def load_function(path: Path, module_name: str) -> Callable[[list[Any]], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_element


def outcome(function: Callable[[list[Any]], Any], value: list[Any]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(value.copy())}
    except Exception as error:  # The exception class is observable at the boundary.
        return {"kind": "raise", "type": type(error).__name__, "message": str(error)}


def add(
    cases: list[tuple[str, list[Any], bool]],
    label: str,
    value: list[Any],
    formal_integer_domain: bool,
) -> None:
    cases.append((label, value, formal_integer_domain))


def main() -> int:
    canonical = load_function(CANONICAL_PATH, "trusted_canonical")
    generated = load_function(GENERATED_PATH, "submitted_solution")
    cases: list[tuple[str, list[Any], bool]] = []

    add(cases, "doctest-1", [1, 2, 3], True)
    add(cases, "doctest-2", [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10], True)
    add(cases, "empty-boundary", [], False)
    add(cases, "singleton-negative", [-7], True)
    add(cases, "singleton-zero", [0], True)
    add(cases, "singleton-positive", [9], True)
    add(cases, "branch-greater", [1, 2], True)
    add(cases, "branch-less", [2, 1], True)
    add(cases, "branch-equal", [2, 2], True)
    add(cases, "later-greater", [4, -2, 9], True)
    add(cases, "later-less", [4, -2, -9], True)
    add(cases, "later-equal", [4, -2, 4], True)
    add(cases, "all-negative", [-9, -2, -14, -2], True)
    add(cases, "all-equal", [4, 4, 4], True)
    add(cases, "machine-int-boundaries", [-(2**63), 2**63 - 1, 0], True)
    add(cases, "arbitrary-precision", [-(10**100), 10**100, 7], True)
    add(cases, "comparable-floats", [-1.5, 2.25, 2.0], False)
    add(cases, "comparable-strings", ["beta", "alpha", "gamma"], False)

    # Exhaust all short lists over a small ordered alphabet. This covers every
    # greater/equal/less transition at every position up to length five.
    alphabet = [-2, -1, 0, 1, 2]
    for length in range(1, 6):
        for index, values in enumerate(itertools.product(alphabet, repeat=length)):
            add(cases, f"exhaustive-len-{length}-{index}", list(values), True)

    # Deterministic broader inputs exercise arbitrary-precision integers and
    # longer lists without sharing implementation logic with either function.
    generator = random.Random(350035)
    for index in range(2000):
        length = generator.randint(1, 40)
        values = [generator.randint(-(10**40), 10**40) for _ in range(length)]
        add(cases, f"generated-{index}", values, True)

    intended_mismatches = 0
    out_of_formal_mismatches = 0
    formal_count = 0
    out_of_formal_count = 0
    with INPUT_LOG.open("w", encoding="utf-8") as stream:
        for index, (label, value, formal_integer_domain) in enumerate(cases):
            expected = outcome(canonical, value)
            actual = outcome(generated, value)
            match = expected == actual
            if formal_integer_domain:
                formal_count += 1
                intended_mismatches += not match
            else:
                out_of_formal_count += 1
                out_of_formal_mismatches += not match
            stream.write(
                json.dumps(
                    {
                        "index": index,
                        "label": label,
                        "input": value,
                        "formal_integer_domain": formal_integer_domain,
                        "canonical": expected,
                        "generated": actual,
                        "match": match,
                    },
                    sort_keys=True,
                )
                + "\n"
            )

    print(f"seed=350035")
    print(f"formal_integer_cases={formal_count}")
    print(f"formal_integer_mismatches={intended_mismatches}")
    print(f"out_of_formal_cases={out_of_formal_count}")
    print(f"out_of_formal_mismatches={out_of_formal_mismatches}")
    print(
        "empty_boundary="
        f"canonical:{outcome(canonical, [])} generated:{outcome(generated, [])}"
    )
    print(f"complete_inputs={INPUT_LOG}")
    return 1 if intended_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
