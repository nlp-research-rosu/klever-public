#!/usr/bin/env python3
"""Independent finite witnesses for the handwritten source/summary comparison.

This does not execute any mounted candidate file.  The branch predicate below is
transcribed from each of the four source `if` statements and the supplied K
`applyCmp("<=", Int, Int)` / BoolOp rules.
"""

DIGITS = (2, 4, 6, 8)


def source_branch(a: int, b: int, d: int) -> bool:
    return (a <= d and d <= b) or (b <= d and d <= a)


def in_closed_span(a: int, b: int, d: int) -> bool:
    return (a <= d and d <= b) or (b <= d and d <= a)


def source_result(a: int, b: int) -> list[int]:
    result = []
    for digit in DIGITS:
        if source_branch(a, b, digit):
            result.append(digit)
    return result


def summary_result(a: int, b: int) -> list[int]:
    return [digit for digit in DIGITS if in_closed_span(a, b, digit)]


mismatches = []
for a in range(-2, 15):
    for b in range(-2, 15):
        if source_result(a, b) != summary_result(a, b):
            mismatches.append((a, b))

print(f"finite_grid_pairs={17 * 17}")
print(f"source_summary_mismatches={len(mismatches)}")
for a, b in [(1, 1), (2, 2), (2, 8), (8, 2), (3, 7), (7, 3), (6, 6), (10, 14)]:
    print(f"witness ({a},{b}) -> {summary_result(a, b)}")

mutations = {
    "hardcoded_empty": (2, 8, []),
    "hardcoded_all": (10, 14, list(DIGITS)),
    "ascending_endpoint_only": (8, 2, []),
    "exclusive_endpoints": (2, 2, []),
    "missing_8": (8, 8, []),
    "reversed_output": (2, 8, list(reversed(DIGITS))),
}
for name, (a, b, mutated) in mutations.items():
    expected = source_result(a, b)
    print(
        f"counterfactual {name}: witness=({a},{b}) "
        f"source={expected} mutated={mutated} rejected={expected != mutated}"
    )

if mismatches:
    raise SystemExit(1)
if not all(source_result(a, b) != mutated for a, b, mutated in mutations.values()):
    raise SystemExit(1)
