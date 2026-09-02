#!/usr/bin/env python3
"""Independent differential test for canonical.py versus submitted solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType


CANONICAL = Path("/tmp/audit-work/rebuild/trusted/canonical.py")
GENERATED = Path("/tmp/audit-work/rebuild/candidate/solution.py")
INPUT_LOG = Path("/audit-output/evidence/differential-inputs.jsonl")


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cases() -> list[tuple[str, list[int]]]:
    # Named cases cover both documented examples, empty input, the comparison
    # boundary at cumulative balances -1/0/+1, delayed failure, early return,
    # and arbitrary-precision integers.
    named = [
        ("documented_positive", [1, 2, 3]),
        ("documented_negative", [1, 2, -4, 5]),
        ("empty", []),
        ("immediate_minus_one", [-1]),
        ("single_zero", [0]),
        ("single_plus_one", [1]),
        ("zero_then_negative", [0, -1]),
        ("exact_zero_boundary", [5, -5]),
        ("one_above_boundary", [5, -4]),
        ("one_below_boundary", [5, -6]),
        ("delayed_negative", [2, -1, -2]),
        ("early_negative_then_recovery", [-1, 100]),
        ("large_exact_zero", [10**100, -(10**100)]),
        ("large_below_zero", [10**100, -(10**100) - 1]),
    ]
    result = list(named)

    # Exhaust every list through length four over values around the branch
    # boundary. This includes 781 lists before de-duplication.
    alphabet = (-2, -1, 0, 1, 2)
    for length in range(5):
        for values in itertools.product(alphabet, repeat=length):
            result.append((f"exhaustive_len_{length}", list(values)))

    # Deterministic broader representatives with variable lengths and values.
    rng = random.Random(0x3B310)
    for _ in range(2000):
        length = rng.randrange(0, 41)
        values = [rng.randrange(-10_000, 10_001) for _ in range(length)]
        result.append(("generated_seed_0x3B310", values))
    return result


def main() -> int:
    canonical = load("trusted_canonical", CANONICAL)
    generated = load("submitted_solution", GENERATED)
    all_cases = cases()
    mismatches: list[dict[str, object]] = []
    canonical_errors = 0
    generated_errors = 0
    with INPUT_LOG.open("w", encoding="utf-8") as stream:
        for index, (category, values) in enumerate(all_cases):
            record: dict[str, object] = {
                "index": index,
                "category": category,
                "input": values,
            }
            try:
                expected = canonical.below_zero(list(values))
                record["canonical"] = expected
            except Exception as error:  # pragma: no cover - evidence path
                canonical_errors += 1
                record["canonical_error"] = repr(error)
                expected = ("error", type(error).__name__, str(error))
            try:
                actual = generated.below_zero(list(values))
                record["generated"] = actual
            except Exception as error:  # pragma: no cover - evidence path
                generated_errors += 1
                record["generated_error"] = repr(error)
                actual = ("error", type(error).__name__, str(error))
            if actual != expected:
                mismatches.append(record)
            stream.write(json.dumps(record, separators=(",", ":")) + "\n")

    print(f"canonical={CANONICAL}")
    print(f"generated={GENERATED}")
    print("oracle=trusted canonical below_zero, independently imported")
    print(
        "scope=14 named boundary/example cases + all 781 sequences of "
        "length 0..4 over [-2,-1,0,1,2] + 2000 deterministic generated lists"
    )
    print(f"seed=0x3B310 total={len(all_cases)}")
    print(
        f"mismatches={len(mismatches)} canonical_errors={canonical_errors} "
        f"generated_errors={generated_errors}"
    )
    for mismatch in mismatches[:20]:
        print("MISMATCH " + json.dumps(mismatch, separators=(",", ":")))
    return 1 if mismatches or canonical_errors or generated_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
