#!/usr/bin/env python3
"""Independent differential audit for HumanEval 126 is_sorted."""

from __future__ import annotations

import importlib.util
import itertools
import json
import pathlib
import random
import sys
from collections import Counter
from collections.abc import Callable


WORK = pathlib.Path("/tmp/audit-work/reconstruction")
INPUT_LOG = pathlib.Path("/audit-output/evidence/02_differential_inputs.jsonl")


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[list[int]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


def direct_contract(values: list[int]) -> bool:
    """Independent reading of the prompt, not either implementation."""
    return all(a <= b for a, b in zip(values, values[1:])) and all(
        multiplicity <= 2 for multiplicity in Counter(values).values()
    )


def main() -> int:
    canonical = load_entry(
        pathlib.Path("/reference/canonical.py"), "trusted_canonical"
    )
    generated = load_entry(WORK / "solution.py", "generated_solution")

    examples = [
        [5],
        [1, 2, 3, 4, 5],
        [1, 3, 2, 4, 5],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 3, 2, 4, 5, 6, 7],
        [1, 2, 2, 3, 3, 4],
        [1, 2, 2, 2, 3, 4],
    ]
    boundaries = [
        [],
        [0],
        [0, 0],
        [0, 0, 0],
        [0, 1],
        [1, 0],
        [1, 1, 2, 2],
        [1, 1, 2, 2, 2],
        [0, 0, 1, 1, 0],
        [0, 1, 1, 2],
        [0, 1, 1, 1, 2],
        [10**100],
        [0, 10**100],
        [10**100, 0],
        [10**100, 10**100],
        [10**100, 10**100, 10**100],
        list(range(8)),
        list(range(40)),
        [7] * 40,
    ]

    grouped: list[tuple[str, list[list[int]]]] = [
        ("documented-example", examples),
        ("boundary-and-branch", boundaries),
        (
            "exhaustive-len-0-through-7-values-0-through-4",
            [
                list(values)
                for length in range(8)
                for values in itertools.product(range(5), repeat=length)
            ],
        ),
    ]

    rng = random.Random(126_20260723)
    random_cases: list[list[int]] = []
    for _ in range(5000):
        length = rng.randrange(0, 41)
        random_cases.append([rng.randrange(0, 101) for _ in range(length)])
    for _ in range(1000):
        length = rng.randrange(0, 41)
        values = sorted(rng.randrange(0, 21) for _ in range(length))
        random_cases.append(values)
    grouped.append(("seeded-generated-len-0-through-40", random_cases))

    mismatches: list[dict[str, object]] = []
    seen: set[tuple[int, ...]] = set()
    total = 0
    with INPUT_LOG.open("w", encoding="utf-8") as input_handle:
        for group, cases in grouped:
            for values in cases:
                key = tuple(values)
                if key in seen:
                    continue
                seen.add(key)
                total += 1
                canonical_result = canonical(values.copy())
                generated_result = generated(values.copy())
                contract_result = direct_contract(values)
                record = {"group": group, "input": values}
                input_handle.write(json.dumps(record, separators=(",", ":")) + "\n")
                if not (
                    canonical_result == generated_result == contract_result
                    and isinstance(generated_result, bool)
                ):
                    mismatches.append(
                        {
                            **record,
                            "canonical": canonical_result,
                            "generated": generated_result,
                            "direct_contract": contract_result,
                            "generated_type": type(generated_result).__name__,
                        }
                    )

    print("oracle=/reference/canonical.py:is_sorted")
    print("generated=/tmp/audit-work/reconstruction/solution.py:is_sorted")
    print(
        "direct_contract=nondecreasing adjacent pairs and every Counter count <= 2"
    )
    print("random_seed=12620260723")
    for group, cases in grouped:
        print(f"declared_group={group}; generated_count={len(cases)}")
    print(f"unique_inputs={total}")
    print(f"input_log={INPUT_LOG}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(json.dumps(mismatch, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
