#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval/4."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random
import struct
from typing import Any, Callable


CANDIDATE = Path("/tmp/audit-work/4-mad-audit/candidate/solution.py")
CANONICAL = Path("/tmp/audit-work/4-mad-audit/trusted/canonical.py")
SEED = 0x4D4144


def load_entry(path: Path, module_name: str) -> Callable[[list[float]], float]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.mean_absolute_deviation


def outcome(function: Callable[[list[float]], float], values: list[float]) -> tuple[Any, ...]:
    try:
        value = function(list(values))
    except BaseException as err:  # Compare the observable exception class and arguments.
        return ("exception", type(err).__module__, type(err).__qualname__, err.args)
    if isinstance(value, float):
        if math.isnan(value):
            return ("float", "nan")
        return ("float", struct.pack(">d", value).hex(), repr(value))
    return ("value", type(value).__qualname__, repr(value))


def main() -> int:
    candidate = load_entry(CANDIDATE, "audit_candidate_solution")
    canonical = load_entry(CANONICAL, "audit_trusted_canonical")

    named_cases: list[tuple[str, list[float]]] = [
        ("documented-example", [1.0, 2.0, 3.0, 4.0]),
        ("empty-boundary", []),
        ("singleton", [5.0]),
        ("all-equal", [2.5, 2.5, 2.5]),
        ("two-values", [-1.0, 1.0]),
        ("abs-below-equal-above-mean", [-2.0, 0.0, 2.0]),
        ("mixed-signs", [-7.25, -0.5, 3.0, 12.75]),
        ("signed-zero", [-0.0, 0.0, -0.0]),
        ("small-magnitudes", [1e-300, -1e-300, 0.0]),
        ("large-safe-magnitudes", [1e150, -1e150, 5e149]),
        ("rounding-sensitive-decimals", [0.1, 0.2, 0.3]),
        ("repeated-rounding", [0.1] * 9 + [0.2]),
        ("positive-infinity", [1.0, float("inf")]),
        ("negative-infinity", [float("-inf"), -1.0]),
        ("nan-element", [1.0, float("nan"), 2.0]),
    ]

    rng = random.Random(SEED)
    pool = [
        -1000.5,
        -17.25,
        -2.0,
        -1.0,
        -0.1,
        -0.0,
        0.0,
        0.1,
        0.2,
        1.0,
        2.0,
        17.25,
        1000.5,
    ]
    generated_cases: list[tuple[str, list[float]]] = []
    for index in range(250):
        length = rng.randint(1, 20)
        values = [
            rng.choice(pool) if rng.random() < 0.55 else rng.uniform(-10000.0, 10000.0)
            for _ in range(length)
        ]
        generated_cases.append((f"generated-{index:03d}", values))

    cases = named_cases + generated_cases
    serializable = [(name, [repr(value) for value in values]) for name, values in cases]
    corpus_hash = hashlib.sha256(
        json.dumps(serializable, separators=(",", ":"), ensure_ascii=True).encode()
    ).hexdigest()
    print(f"seed={SEED}")
    print(f"case_count={len(cases)} corpus_sha256={corpus_hash}")

    mismatches = 0
    for index, (name, values) in enumerate(cases):
        expected = outcome(canonical, values)
        actual = outcome(candidate, values)
        same = actual == expected
        print(
            f"CASE {index:03d} {name} input={values!r} "
            f"canonical={expected!r} candidate={actual!r} same={same}"
        )
        mismatches += int(not same)

    print(f"mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
