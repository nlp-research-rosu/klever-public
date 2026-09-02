#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import random
from typing import Any, Callable


def load_function(path: str) -> Callable[[str, int], int]:
    spec = importlib.util.spec_from_file_location(Path(path).stem + "_audit", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fruit_distribution


def outcome(function: Callable[[str, int], int], s: str, n: int) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(s, n)}
    except Exception as error:  # Comparison intentionally records exceptional boundaries.
        return {"kind": "error", "type": type(error).__name__, "message": str(error)}


def main() -> int:
    canonical = load_function("/reference/canonical.py")
    candidate = load_function("/candidate/solution.py")
    cases: list[tuple[str, int, str]] = [
        ("5 apples and 6 oranges", 19, "prompt-example"),
        ("0 apples and 1 oranges", 3, "prompt-example"),
        ("2 apples and 3 oranges", 100, "prompt-example"),
        ("100 apples and 1 oranges", 120, "prompt-example"),
        ("0 apples and 0 oranges", 0, "valid-boundary"),
        ("0 apples and 0 oranges", 1, "valid-boundary"),
        ("9 apples and 10 oranges", 19, "valid-boundary"),
        ("0005 apples and 0006 oranges", 19, "valid-leading-zero"),
        ("5  apples  and  6  oranges", 19, "valid-extra-ascii-spaces"),
        (" 5 apples and 6 oranges ", 19, "valid-leading-trailing-spaces"),
        ("5 apples and 6 oranges.", 19, "valid-punctuation"),
        ("", 7, "empty-boundary"),
        ("apples and oranges", 7, "no-digit-boundary"),
        ("5 apples 6 oranges", 19, "alternate-grammatical-shape"),
        ("there are 5 apples and 6 oranges", 19, "alternate-grammatical-shape"),
        ("apples 5 and oranges 6", 19, "alternate-grammatical-shape"),
        ("5 apples and 6 oranges and 2 labels", 19, "additional-digit-token"),
        ("5\tapples and 6 oranges", 19, "non-space-whitespace"),
        ("-5 apples and 6 oranges", 19, "signed-number-boundary"),
    ]

    # Deterministic broad sample over the exact five-token sentence grammar.
    rng = random.Random(670067)
    values = [0, 1, 2, 9, 10, 99, 100, 10**6, 10**30]
    for a in values:
        for b in values:
            for slack in (0, 1, 17):
                cases.append((f"{a} apples and {b} oranges", a + b + slack, "grid-valid"))
    for _ in range(200):
        a = rng.randrange(0, 10**50)
        b = rng.randrange(0, 10**50)
        slack = rng.randrange(0, 10**30)
        cases.append((f"{a} apples and {b} oranges", a + b + slack, "random-valid"))

    mismatches: list[dict[str, Any]] = []
    counts: dict[str, dict[str, int]] = {}
    for index, (s, n, category) in enumerate(cases):
        left = outcome(canonical, s, n)
        right = outcome(candidate, s, n)
        counts.setdefault(category, {"cases": 0, "mismatches": 0})
        counts[category]["cases"] += 1
        if left != right:
            counts[category]["mismatches"] += 1
            mismatches.append(
                {
                    "index": index,
                    "category": category,
                    "s": s,
                    "n": n,
                    "canonical": left,
                    "candidate": right,
                }
            )

    print(
        json.dumps(
            {
                "oracle": "/reference/canonical.py::fruit_distribution",
                "subject": "/candidate/solution.py::fruit_distribution",
                "seed": 670067,
                "counts": counts,
                "total_cases": len(cases),
                "total_mismatches": len(mismatches),
                "mismatches": mismatches,
            },
            indent=2,
            sort_keys=True,
        )
    )
    # Mismatches are evidence to assess, not a harness failure.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
