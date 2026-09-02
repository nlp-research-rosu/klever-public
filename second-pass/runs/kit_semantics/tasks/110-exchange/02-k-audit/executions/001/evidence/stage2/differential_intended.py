#!/usr/bin/env python3
"""Differential check on the ordinary non-empty integer-list contract domain."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable


WORK = Path("/tmp/audit-work/scratch/proof")
INPUT_RECORD = Path(
    "/audit-output/evidence/stage2/differential-intended-inputs.txt"
)


def load_function(path: Path, module_name: str) -> Callable[..., str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exchange


def main() -> None:
    canonical = load_function(WORK / "canonical.py", "trusted_canonical_int")
    generated = load_function(WORK / "solution.py", "generated_solution_int")

    explicit: list[tuple[list[int], list[int], str, str]] = [
        ([1, 2, 3, 4], [1, 2, 3, 4], "YES", "documented-example-yes"),
        ([1, 2, 3, 4], [1, 5, 3, 4], "NO", "documented-example-no"),
        ([2], [1], "YES", "already-even-at-threshold"),
        ([1], [2], "YES", "exchange-at-threshold"),
        ([1], [1], "NO", "one-below-threshold"),
        ([1, 3, 2], [5, 4], "NO", "combined-even-count-len-minus-one"),
        ([1, 3, 2], [4, 6], "YES", "combined-even-count-equals-len"),
        ([2, 4, 6], [8], "YES", "combined-even-count-above-len"),
        ([-4, -3], [-2], "YES", "negative-boundary"),
        ([10**100 + 1], [-(10**100)], "YES", "unbounded-python-int"),
    ]
    robustness: list[tuple[list[int], list[int], str, str]] = [
        ([], [], "YES", "both-empty-outside-precondition"),
        ([], [1], "YES", "empty-lst1-outside-precondition"),
        ([1], [], "NO", "empty-lst2-outside-precondition"),
    ]

    cases: list[tuple[list[int], list[int], str | None, str]] = [
        *explicit,
        *robustness,
    ]

    values = [-2, -1, 0, 1, 2]
    small_lists = [
        list(items)
        for length in range(0, 4)
        for items in itertools.product(values, repeat=length)
    ]
    for left in small_lists:
        for right in small_lists:
            cases.append((left, right, None, "exhaustive-small-int"))

    seed = 110
    randomizer = random.Random(seed)
    for _ in range(10000):
        left = [
            randomizer.randint(-(10**40), 10**40)
            for _ in range(randomizer.randint(1, 20))
        ]
        right = [
            randomizer.randint(-(10**40), 10**40)
            for _ in range(randomizer.randint(1, 20))
        ]
        cases.append((left, right, None, "seeded-unbounded-int"))

    lines = [
        f"{index:05d}\t{tag}\tleft={left!r}\tright={right!r}\texpected={expected!r}"
        for index, (left, right, expected, tag) in enumerate(cases)
    ]
    text = "\n".join(lines) + "\n"
    INPUT_RECORD.write_text(text)
    inputs_hash = hashlib.sha256(text.encode()).hexdigest()

    mismatches = []
    expectation_failures = []
    for index, (left, right, expected, tag) in enumerate(cases):
        oracle = canonical(list(left), list(right))
        observed = generated(list(left), list(right))
        if oracle != observed:
            mismatches.append((index, tag, left, right, oracle, observed))
        if expected is not None and oracle != expected:
            expectation_failures.append((index, tag, expected, oracle))

    print("domain=finite Python int lists; non-empty for contract cases")
    print("robustness=three empty-list cases outside stated precondition")
    print("oracle=/tmp/audit-work/scratch/proof/canonical.py")
    print("candidate=/tmp/audit-work/scratch/proof/solution.py")
    print(f"seed={seed}")
    print(f"cases={len(cases)}")
    print(f"inputs_sha256={inputs_hash}")
    print(f"input_record={INPUT_RECORD}")
    print(f"mismatches={len(mismatches)}")
    print(f"expectation_failures={len(expectation_failures)}")
    for item in mismatches[:20]:
        print("MISMATCH", repr(item))
    for item in expectation_failures[:20]:
        print("EXPECTATION_FAILURE", repr(item))
    if mismatches or expectation_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
