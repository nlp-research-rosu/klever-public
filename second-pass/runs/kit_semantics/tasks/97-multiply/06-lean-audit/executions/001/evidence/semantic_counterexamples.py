#!/usr/bin/env python3


def trunc_remainder(left: int, right: int) -> int:
    quotient = abs(left) // abs(right)
    if (left < 0) != (right < 0):
        quotient = -quotient
    return left - quotient * right


def k_py_mod(left: int, right: int) -> int:
    return trunc_remainder(
        trunc_remainder(left, right) + right,
        right,
    )


def frozen_source_formula(a: int, b: int) -> int:
    return (a % 10) * (b % 10)


def frozen_k_postcondition(a: int, b: int) -> int:
    return k_py_mod(a, 10) * k_py_mod(b, 10)


samples = [
    (-11, -12),
    (-1, 2),
    (0, 123),
    (17, 28),
    (10**50 + 9, -(10**50 + 3)),
]
for a, b in samples:
    source = frozen_source_formula(a, b)
    k_post = frozen_k_postcondition(a, b)
    mutations = {
        "constant_zero": 0,
        "identity_a": a,
        "omit_mod": a * b,
        "sum_digits": (a % 10) + (b % 10),
    }
    print({
        "a": a,
        "b": b,
        "source": source,
        "k_postcondition": k_post,
        "equal": source == k_post,
        "counterfactual_mismatches": {
            name: value != source for name, value in mutations.items()
        },
    })

mismatches = []
for a in range(-100, 101):
    for b in range(-100, 101):
        if frozen_source_formula(a, b) != frozen_k_postcondition(a, b):
            mismatches.append((a, b))

print({
    "grid": "a,b in [-100,100]",
    "cases": 201 * 201,
    "mismatch_count": len(mismatches),
})
raise SystemExit(0 if not mismatches else 1)
