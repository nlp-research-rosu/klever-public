#!/usr/bin/env python3
"""Independent differential tests for HumanEval/5.

The oracle and candidate are imported from paths supplied on the command line.
The test set includes the documented examples, all small lists over a bounded
integer alphabet, seeded broader samples, and cases around CPython's recursion
limit because the candidate is recursive while the canonical implementation is
iterative.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int], int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersperse


def outcome(fn: Callable[[list[int], int], list[int]], values: list[int], delim: int) -> tuple[str, Any]:
    try:
        result = fn(values.copy(), delim)
    except BaseException as error:  # Audit behavior includes Python exceptions.
        return ("exception", type(error).__name__)
    return ("return", result)


def summary(value: tuple[str, Any]) -> dict[str, Any]:
    kind, payload = value
    if kind == "exception":
        return {"kind": kind, "type": payload}
    encoded = json.dumps(payload, separators=(",", ":")).encode()
    return {
        "kind": kind,
        "length": len(payload),
        "first": payload[:4],
        "last": payload[-4:],
        "sha256": hashlib.sha256(encoded).hexdigest(),
    }


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANONICAL_PY CANDIDATE_PY", file=sys.stderr)
        return 64
    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical")
    candidate = load_entry(Path(sys.argv[2]), "audited_candidate")

    cases: list[tuple[str, list[int], int]] = [
        ("documented-empty", [], 4),
        ("documented-three", [1, 2, 3], 4),
        ("singleton", [7], -3),
        ("branch-length-two", [7, -8], 0),
        ("duplicates", [2, 2, 2, 2], 2),
        ("large-integers", [-(10**80), 0, 10**100], -(10**120)),
    ]

    # Exhaust all lists of lengths 0..6 over three representative integers.
    for length in range(7):
        for values in itertools.product((-1, 0, 2), repeat=length):
            for delim in (-3, 0, 5):
                cases.append((f"exhaustive-small-len-{length}", list(values), delim))

    # A deterministic broader sample of ordinary finite values.
    rng = random.Random(0x5EED)
    for index in range(300):
        length = rng.randrange(0, 80)
        values = [rng.randrange(-(10**9), 10**9 + 1) for _ in range(length)]
        delim = rng.randrange(-(10**12), 10**12 + 1)
        cases.append((f"seeded-{index}", values, delim))

    recursion_limit = sys.getrecursionlimit()
    for length in (recursion_limit - 50, recursion_limit - 10, recursion_limit, recursion_limit + 1, recursion_limit + 100):
        cases.append((f"recursion-boundary-{length}", list(range(length)), -11))

    mismatches: list[dict[str, Any]] = []
    for label, values, delim in cases:
        expected = outcome(canonical, values, delim)
        actual = outcome(candidate, values, delim)
        if expected != actual:
            mismatches.append(
                {
                    "label": label,
                    "input_length": len(values),
                    "delimiter": delim,
                    "canonical": summary(expected),
                    "candidate": summary(actual),
                }
            )

    print(f"PYTHON_VERSION {sys.version.split()[0]}")
    print(f"RECURSION_LIMIT {recursion_limit}")
    print(f"CASES {len(cases)}")
    print(f"MISMATCHES {len(mismatches)}")
    for mismatch in mismatches:
        print("MISMATCH " + json.dumps(mismatch, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
