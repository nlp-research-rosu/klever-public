#!/usr/bin/env python3
"""Independent differential check for trusted canonical.py vs submitted solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import json
import math
import random
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/candidate-src/solution.py")


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function: Callable[[Any, Any], Any], a: Any, b: Any) -> dict[str, str]:
    try:
        result = function(a, b)
        return {
            "kind": "return",
            "type": type(result).__name__,
            "repr": repr(result),
        }
    except Exception as error:  # Differential comparison includes boundary exceptions.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "repr": str(error),
        }


def encode(value: Any) -> dict[str, str]:
    return {"type": type(value).__name__, "repr": repr(value)}


def main() -> int:
    canonical = load(CANONICAL_PATH, "trusted_canonical").compare_one
    generated = load(GENERATED_PATH, "submitted_solution").compare_one

    documented = [
        (1, 2.5),
        (1, "2,3"),
        ("5,1", "6"),
        ("1", 1),
    ]
    branch_and_boundary = [
        (0, 0),
        (-1, 0),
        (0, -1),
        (1.0, 1),
        (-0.0, 0),
        ("0", "-0,0"),
        ("1.000", 1.0),
        ("-2,5", -2.0),
        (-3.0, "-3,5"),
        ("1e2", 99),
        (2**53, 2**53 + 1),
        (2**53 + 1, 2**53),
        (-(2**53), -(2**53 + 1)),
        (10**400, 1),
        (1, 10**400),
        ("", 0),          # empty-string robustness boundary, outside documented domain
        (" ", 0),         # whitespace converts to neither a real nor float
        ("1,2,3", 0),     # malformed comma spelling
    ]

    random.seed(137)
    random_ints = [random.randint(-10**6, 10**6) for _ in range(30)]
    atoms: list[Any] = [
        -1000,
        -2,
        -1,
        0,
        1,
        2,
        1000,
        2**53 - 1,
        2**53,
        2**53 + 1,
        -(2**53 + 1),
        -2.5,
        -0.5,
        0.0,
        0.5,
        2.5,
        1e-300,
        1e300,
        "-1000",
        "-2",
        "-0,5",
        "0",
        "0.0",
        "0,5",
        "2",
        "2.5",
        "2,5",
        "1e-300",
        "1e300",
        "9007199254740992",
        "9007199254740993",
    ]
    for value in random_ints:
        atoms.extend((value, str(value), f"{value},25"))

    cases: list[tuple[Any, Any, str]] = []
    cases.extend((a, b, "documented") for a, b in documented)
    cases.extend((a, b, "branch-boundary") for a, b in branch_and_boundary)
    cases.extend((a, b, "representative-cross-product") for a, b in itertools.product(atoms, repeat=2))

    mismatches: list[dict[str, Any]] = []
    by_group: dict[str, int] = {}
    for index, (a, b, group) in enumerate(cases):
        by_group[group] = by_group.get(group, 0) + 1
        expected = outcome(canonical, a, b)
        actual = outcome(generated, a, b)
        if expected != actual:
            mismatches.append(
                {
                    "index": index,
                    "group": group,
                    "a": encode(a),
                    "b": encode(b),
                    "canonical": expected,
                    "generated": actual,
                }
            )

    print(f"CANONICAL={CANONICAL_PATH}")
    print(f"GENERATED={GENERATED_PATH}")
    print("RANDOM_SEED=137")
    print("DOCUMENTED_INPUTS_JSON=" + json.dumps([[encode(a), encode(b)] for a, b in documented]))
    print("BOUNDARY_INPUTS_JSON=" + json.dumps([[encode(a), encode(b)] for a, b in branch_and_boundary]))
    print("REPRESENTATIVE_ATOMS_JSON=" + json.dumps([encode(value) for value in atoms]))
    print("GROUP_COUNTS_JSON=" + json.dumps(by_group, sort_keys=True))
    print(f"TOTAL_CASES={len(cases)}")
    print(f"MISMATCH_COUNT={len(mismatches)}")
    for mismatch in mismatches[:100]:
        print("MISMATCH=" + json.dumps(mismatch, sort_keys=True))
    if len(mismatches) > 100:
        print(f"MISMATCH_OUTPUT_TRUNCATED={len(mismatches) - 100}")

    # A mismatch is a candidate-fidelity failure, so make the evidence command fail.
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
