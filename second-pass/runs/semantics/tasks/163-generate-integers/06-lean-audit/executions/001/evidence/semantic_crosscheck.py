def source_shape(a: int, b: int) -> list[int]:
    result = []
    for digit in (2, 4, 6, 8):
        if (a <= digit <= b) or (b <= digit <= a):
            result.append(digit)
    return result


def between_endpoints(a: int, b: int, digit: int) -> bool:
    return (a <= digit and digit <= b) or (
        b <= digit and digit <= a
    )


def summary_shape(a: int, b: int) -> list[int]:
    rest = []
    for digit in (8, 6, 4, 2):
        if between_endpoints(a, b, digit):
            rest = [digit] + rest
    return rest


pairs = [(a, b) for a in range(1, 21) for b in range(1, 21)]
mismatches = [
    (a, b, source_shape(a, b), summary_shape(a, b))
    for a, b in pairs
    if source_shape(a, b) != summary_shape(a, b)
]
print("positive_domain_pairs_checked", len(pairs))
print("source_summary_mismatches", len(mismatches))
print("boundary_witnesses")
for pair in [(2, 2), (8, 2), (10, 14), (3, 7), (1, 9)]:
    print(pair, source_shape(*pair), summary_shape(*pair))


def forward_only(a: int, b: int) -> list[int]:
    return [digit for digit in (2, 4, 6, 8) if a <= digit <= b]


def strict_endpoints(a: int, b: int) -> list[int]:
    low, high = min(a, b), max(a, b)
    return [digit for digit in (2, 4, 6, 8) if low < digit < high]


def hard_coded(_a: int, _b: int) -> list[int]:
    return [2, 4, 6, 8]


def reversed_order(a: int, b: int) -> list[int]:
    return [
        digit
        for digit in (8, 6, 4, 2)
        if between_endpoints(a, b, digit)
    ]


print("counterfactual_mutations")
for name, mutation, pair in [
    ("forward_only", forward_only, (8, 2)),
    ("strict_endpoints", strict_endpoints, (2, 2)),
    ("hard_coded", hard_coded, (10, 14)),
    ("reversed_order", reversed_order, (3, 7)),
]:
    print(
        name,
        pair,
        "expected=" + str(source_shape(*pair)),
        "mutated=" + str(mutation(*pair)),
        "rejected=" + str(source_shape(*pair) != mutation(*pair)),
    )
