#!/usr/bin/env python3
"""Independent source-domain differential check for HumanEval 116."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


canonical = load_entry(
    Path("/tmp/audit-work/reconstruction/canonical.py"), "trusted_canonical"
)
generated = load_entry(
    Path("/tmp/audit-work/reconstruction/solution.py"), "generated_solution"
)

checked = 0
mismatches: list[tuple[list[int], list[int], list[int]]] = []


def check_intended(values: list[int]) -> None:
    global checked
    original = list(values)
    canonical_result = canonical(values)
    generated_result = generated(values)
    if values != original:
        raise AssertionError(f"input mutated: {original!r} -> {values!r}")
    if generated_result != canonical_result:
        mismatches.append((original, canonical_result, generated_result))
    checked += 1


named_cases = {
    "empty": [],
    "zero boundary": [0],
    "nonnegative branch boundary": [0, 1],
    "prompt example 1 input": [1, 5, 2, 3, 4],
    "prompt example 3 input": [1, 0, 2, 3, 4],
    "duplicates": [7, 7, 0, 3, 3, 8, 8, 1],
    "same-popcount tie": [12, 10, 9, 6, 5, 3],
    "powers and neighbors": [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 63, 64],
    "large integers": [
        (1 << 64) - 1,
        1 << 64,
        (1 << 127) + (1 << 63) + 1,
        (1 << 512) - 1,
    ],
}
for name, values in named_cases.items():
    check_intended(list(values))
    print(
        f"NAMED {name}: canonical={canonical(list(values))!r} "
        f"generated={generated(list(values))!r}"
    )

for length in range(5):
    for values in itertools.product(range(9), repeat=length):
        check_intended(list(values))

rng = random.Random(0x116)
for _ in range(2000):
    length = rng.randrange(0, 80)
    values = [rng.getrandbits(rng.randrange(0, 257)) for _ in range(length)]
    check_intended(values)

# The implementation contains a negative-input branch, so exercise both sides
# of its -1/0 boundary. Negative integers are explicitly outside the prose
# contract; their divergence from the canonical function is reported, not
# counted as an in-domain mismatch.
for values in ([-1], [-2, -3, -4, -5, -6], [-1, 0, 1], [-8, -7, -4, -3]):
    print(
        f"OUT_OF_DOMAIN {values!r}: canonical={canonical(list(values))!r} "
        f"generated={generated(list(values))!r}"
    )

prompt_examples = [
    ([1, 5, 2, 3, 4], [1, 2, 3, 4, 5]),
    ([-2, -3, -4, -5, -6], [-6, -5, -4, -3, -2]),
    ([1, 0, 2, 3, 4], [0, 1, 2, 3, 4]),
]
for values, displayed in prompt_examples:
    print(
        f"PROMPT_DISPLAY {values!r}: displayed={displayed!r} "
        f"canonical={canonical(list(values))!r} "
        f"generated={generated(list(values))!r}"
    )

print(f"INTENDED_DOMAIN_CASES {checked}")
print(f"INTENDED_DOMAIN_MISMATCHES {len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
