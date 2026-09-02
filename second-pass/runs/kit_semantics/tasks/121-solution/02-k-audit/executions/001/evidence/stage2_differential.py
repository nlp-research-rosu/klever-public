#!/usr/bin/env python3
"""Independent differential test for HumanEval/121.

The trusted oracle and candidate are loaded from the isolated reconstruction
copy.  The test input stream is preserved as JSON Lines at the supplied path.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import pathlib
import random
import sys
from collections.abc import Callable, Iterator


WORK = pathlib.Path("/tmp/audit-work/reconstruction")
INPUT_LOG = pathlib.Path(sys.argv[1])
SEED = 121_20260729


def load_solution(path: pathlib.Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solution


oracle = load_solution(WORK / "canonical.py", "trusted_canonical_121")
candidate = load_solution(WORK / "solution.py", "candidate_solution_121")

documented: list[tuple[list[int], int]] = [
    ([5, 8, 7, 1], 12),
    ([3, 3, 3, 3, 3], 9),
    ([30, 13, 24, 321], 0),
]

boundaries: list[list[int]] = [
    [],
    [0],
    [1],
    [2],
    [-1],
    [-2],
    [1, 3],
    [2, 3],
    [1, 2, 3],
    [2, 1, 4, 3],
    [-3, -2, -1, 0, 1, 2, 3],
    [10**100 + 1, -(10**100 + 1), -(10**100 + 3)],
]


def all_cases() -> Iterator[tuple[str, list[int], int | None]]:
    for case, expected in documented:
        yield "documented", case, expected
    for case in boundaries:
        yield "boundary", case, None
    values = range(-3, 4)
    for length in range(0, 7):
        for values_tuple in itertools.product(values, repeat=length):
            yield "exhaustive[-3,3],len[0,6]", list(values_tuple), None
    rng = random.Random(SEED)
    edge_values = [
        -(10**100 + 3),
        -(2**63),
        -10**9 - 1,
        -3,
        -2,
        -1,
        0,
        1,
        2,
        3,
        10**9 + 1,
        2**63,
        10**100 + 1,
    ]
    for _ in range(5000):
        length = rng.randint(1, 100)
        case = [
            rng.choice(edge_values)
            if rng.randrange(4) == 0
            else rng.randint(-(10**12), 10**12)
            for _ in range(length)
        ]
        yield "random(seed=12120260729,len[1,100])", case, None


category_counts: dict[str, int] = {}
mismatches: list[dict[str, object]] = []
digest = hashlib.sha256()
INPUT_LOG.parent.mkdir(parents=True, exist_ok=True)
with INPUT_LOG.open("w", encoding="utf-8") as input_stream:
    for number, (category, case, expected) in enumerate(all_cases(), 1):
        record = {"n": number, "category": category, "input": case}
        encoded = json.dumps(record, separators=(",", ":"), ensure_ascii=False)
        input_stream.write(encoded + "\n")
        digest.update((encoded + "\n").encode())
        category_counts[category] = category_counts.get(category, 0) + 1
        oracle_result = oracle(case)
        candidate_result = candidate(case)
        if expected is not None and oracle_result != expected:
            mismatches.append(
                {
                    "n": number,
                    "kind": "oracle-vs-example",
                    "input": case,
                    "oracle": oracle_result,
                    "expected": expected,
                }
            )
        if candidate_result != oracle_result:
            mismatches.append(
                {
                    "n": number,
                    "kind": "candidate-vs-oracle",
                    "input": case,
                    "candidate": candidate_result,
                    "oracle": oracle_result,
                }
            )

print("oracle", WORK / "canonical.py")
print("candidate", WORK / "solution.py")
print("seed", SEED)
print("category_counts", json.dumps(category_counts, sort_keys=True))
print("total_cases", sum(category_counts.values()))
print("input_jsonl", INPUT_LOG)
print("input_jsonl_sha256", digest.hexdigest())
print("mismatch_count", len(mismatches))
for mismatch in mismatches[:20]:
    print("MISMATCH", json.dumps(mismatch, ensure_ascii=False, sort_keys=True))
sys.exit(1 if mismatches else 0)
