#!/usr/bin/env python3
"""Independent differential check for HumanEval 57-monotonic.

Oracle: the trusted /reference/canonical.py entry point.
Candidate: the copied /tmp/audit-work/review-57/src/solution.py entry point.
Generated scope: all lists of lengths 0..7 over [-2, -1, 0, 1, 2].
"""

from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path


def load_module(name: str, path: Path):
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module(
    "trusted_canonical", Path("/tmp/audit-work/review-57/trusted/canonical.py")
)
candidate = load_module(
    "candidate_solution", Path("/tmp/audit-work/review-57/src/solution.py")
)

documented_and_boundaries = [
    [1, 2, 4, 20],
    [1, 20, 4, 10],
    [4, 1, 0, -10],
    [],
    [0],
    [1, 1],
    [1, 2],
    [2, 1],
    [1, 1, 1],
    [-1, 0, 0, 2],
    [2, 0, 0, -1],
    [0, 1, 0],
    [1, 0, 1],
    [-(10**100), 0, 10**100],
    [10**100, 0, -(10**100)],
]


def check(xs):
    expected = canonical.monotonic(xs)
    actual = candidate.monotonic(xs)
    if actual != expected:
        raise AssertionError(f"mismatch input={xs!r} canonical={expected!r} candidate={actual!r}")
    # A separate characterization helps detect accidental shared failure.
    relation_oracle = (
        all(a <= b for a, b in zip(xs, xs[1:]))
        or all(a >= b for a, b in zip(xs, xs[1:]))
    )
    if actual != relation_oracle:
        raise AssertionError(
            f"relation mismatch input={xs!r} relation={relation_oracle!r} candidate={actual!r}"
        )
    return actual


print("EXPLICIT_CASES")
for case in documented_and_boundaries:
    print(f"{case!r} -> {check(case)!r}")

alphabet = (-2, -1, 0, 1, 2)
tested = 0
true_count = 0
false_count = 0
for length in range(8):
    for values in product(alphabet, repeat=length):
        result = check(list(values))
        tested += 1
        true_count += int(result)
        false_count += int(not result)

print("GENERATED_SCOPE: lengths=0..7 alphabet=(-2,-1,0,1,2)")
print(f"GENERATED_TESTS: {tested}")
print(f"TRUE_RESULTS: {true_count}")
print(f"FALSE_RESULTS: {false_count}")
print("MISMATCHES: 0")
