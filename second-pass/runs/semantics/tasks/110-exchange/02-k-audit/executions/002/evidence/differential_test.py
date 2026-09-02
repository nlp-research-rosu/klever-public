#!/usr/bin/env python3
import importlib.util
import itertools
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/review")


def load_function(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.exchange


canonical = load_function("trusted_canonical_110", ROOT / "canonical.py")
generated = load_function("generated_solution_110", ROOT / "solution.py")


def independent_oracle(first, second):
    odd_first = sum(1 for value in first if value % 2 == 1)
    even_second = sum(1 for value in second if value % 2 == 0)
    return "YES" if odd_first <= even_second else "NO"


named_cases = [
    ("documented_yes", [1, 2, 3, 4], [1, 2, 3, 4]),
    ("documented_no", [1, 2, 3, 4], [1, 5, 3, 4]),
    ("empty_both_excluded_boundary", [], []),
    ("empty_first_excluded_boundary", [], [1]),
    ("empty_second_excluded_boundary", [1], []),
    ("equal_zero_zero", [2], [1]),
    ("equal_one_one", [1], [2]),
    ("less_than", [2, 4], [2]),
    ("greater_than", [1, 3], [2]),
    ("negative_parity", [-3, -2], [-4, 5]),
    ("zeros", [0, 0], [0]),
    ("large_magnitude", [10**80 + 1, -(10**80 + 1)], [10**100]),
]

mismatches = []
yes_count = 0
no_count = 0


def check(label, first, second, verbose=False):
    global yes_count, no_count
    expected = independent_oracle(first, second)
    trusted = canonical(first, second)
    actual = generated(first, second)
    if actual == "YES":
        yes_count += 1
    else:
        no_count += 1
    if verbose:
        print(
            f"CASE {label}: first={first!r} second={second!r} "
            f"canonical={trusted!r} generated={actual!r} oracle={expected!r}"
        )
    if trusted != actual or trusted != expected:
        mismatches.append((label, first, second, trusted, actual, expected))


for label, first, second in named_cases:
    check(label, first, second, verbose=True)

alphabet = [-2, -1, 0, 1, 2]
small_lists = [[]]
for length in range(1, 4):
    small_lists.extend([list(values) for values in itertools.product(alphabet, repeat=length)])
for first_index, first in enumerate(small_lists):
    for second_index, second in enumerate(small_lists):
        check(f"exhaustive_{first_index}_{second_index}", first, second)

rng = random.Random(110)
for index in range(5000):
    first = [rng.randint(-10**12, 10**12) for _ in range(rng.randint(0, 20))]
    second = [rng.randint(-10**12, 10**12) for _ in range(rng.randint(0, 20))]
    check(f"random_{index}", first, second)

total = len(named_cases) + len(small_lists) ** 2 + 5000
print(
    f"SUMMARY total={total} named={len(named_cases)} "
    f"exhaustive_pairs={len(small_lists) ** 2} random=5000 "
    f"yes={yes_count} no={no_count} mismatches={len(mismatches)}"
)
if mismatches:
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    raise SystemExit(1)
