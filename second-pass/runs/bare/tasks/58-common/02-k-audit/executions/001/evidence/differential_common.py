#!/usr/bin/env python3
"""Independent differential test for HumanEval 58 common()."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(
    Path("/tmp/audit-work/58-common/solution.py"), "scratch_generated"
)

documented_and_boundary = [
    ([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121]),
    ([5, 3, 2, 8], [3, 2]),
    ([], []),
    ([], [0]),
    ([0], []),
    ([0], [0]),
    ([0], [1]),
    ([1, 1, 1], [1, 1]),
    ([3, 2, 1], [1, 2, 3]),
    ([-3, -1, 0, 2], [-4, -3, 0, 9]),
    ([10**100, -(10**100), 0], [10**100, 1, -(10**100)]),
    ([2, 1, 2, 3], [3, 2, 3, 4]),
]

small_values = (-2, 0, 1, 2)
small_lists = [
    list(items)
    for length in range(4)
    for items in itertools.product(small_values, repeat=length)
]

rng = random.Random(580058)
random_pairs = [
    (
        [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 20))],
        [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 20))],
    )
    for _ in range(1000)
]

all_pairs = (
    documented_and_boundary
    + [(left, right) for left in small_lists for right in small_lists]
    + random_pairs
)

mismatches = []
for index, (left, right) in enumerate(all_pairs):
    expected = canonical(list(left), list(right))
    actual = generated(list(left), list(right))
    if actual != expected:
        mismatches.append(
            {
                "index": index,
                "left": left,
                "right": right,
                "canonical": expected,
                "generated": actual,
            }
        )

print("documented_and_boundary_inputs=" + json.dumps(documented_and_boundary))
print(f"exhaustive_values={small_values}")
print("exhaustive_lengths=0..3")
print(f"exhaustive_list_count={len(small_lists)}")
print(f"exhaustive_pair_count={len(small_lists) ** 2}")
print("random_seed=580058")
print("random_pair_count=1000")
print(f"total_pair_count={len(all_pairs)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print("first_mismatches=" + json.dumps(mismatches[:20]))
    raise SystemExit(1)
