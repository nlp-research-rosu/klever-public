#!/usr/bin/env python3
"""Finite guard/overlap witnesses supporting the manual proof-rule audit."""


def py_mod(value: int, divisor: int) -> int:
    return ((value % divisor) + divisor) % divisor


def digit_math(accumulator: int, value: int) -> int:
    if value <= 0:
        return accumulator
    return accumulator + str(value).count("7")


def fizz_math(accumulator: int, bound: int) -> int:
    if bound <= 0:
        return accumulator
    return accumulator + sum(
        str(candidate).count("7")
        for candidate in range(bound)
        if candidate % 11 == 0 or candidate % 13 == 0
    )


checked_digit = 0
checked_fizz = 0
boundary_fold_overlaps = 0
for accumulator in (-9, 0, 4, 100):
    for value in range(-100, 10_001):
        base = value <= 0
        positive = value > 0
        if base == positive:
            raise AssertionError(("digit guard coverage", value))
        if base and digit_math(accumulator, value) != accumulator:
            raise AssertionError(("digit base", accumulator, value))
        if positive:
            remainder = py_mod(value, 10)
            quotient = (value - remainder) // 10
            bit = int(remainder == 7)
            if not 0 <= quotient < value:
                raise AssertionError(("digit descent", value, quotient))
            lhs = digit_math(accumulator + bit, quotient)
            rhs = digit_math(accumulator, value)
            if lhs != rhs:
                raise AssertionError(("digit fold", accumulator, value, lhs, rhs))
            if quotient <= 0:
                boundary_fold_overlaps += 1
                boundary_rhs = accumulator + bit
                if boundary_rhs != rhs:
                    raise AssertionError(
                        ("digit boundary overlap", accumulator, value, boundary_rhs, rhs)
                    )
        checked_digit += 1

for accumulator in (-9, 0, 4, 100):
    for bound in range(-100, 10_001):
        base = bound <= 0
        positive = bound > 0
        if base == positive:
            raise AssertionError(("fizz guard coverage", bound))
        if base and fizz_math(accumulator, bound) != accumulator:
            raise AssertionError(("fizz base", accumulator, bound))
        if positive:
            candidate = bound - 1
            qualifying = py_mod(candidate, 11) == 0 or py_mod(candidate, 13) == 0
            nonqualifying = not qualifying
            if qualifying == nonqualifying:
                raise AssertionError(("fizz branch partition", bound))
            if not 0 <= candidate < bound:
                raise AssertionError(("fizz descent", bound, candidate))
            previous = fizz_math(accumulator, candidate)
            lhs_accumulator = (
                digit_math(accumulator, candidate) if qualifying else accumulator
            )
            lhs = fizz_math(lhs_accumulator, candidate)
            rhs = fizz_math(accumulator, bound)
            if lhs != rhs:
                raise AssertionError(
                    ("fizz fold", accumulator, bound, qualifying, lhs, rhs)
                )
        checked_fizz += 1

verification = open("/tmp/audit-work/36-fizz-buzz/verification.k").read()
for forbidden in (
    "<k>",
    "Call(",
    "While(",
    "#while(",
    "Assign(",
    "Return(",
    "closureVal(",
):
    if forbidden in verification:
        raise AssertionError(f"proof-local operational interception found: {forbidden}")

print(f"digit_equation_ground_checks={checked_digit}")
print(f"digit_boundary_fold_overlap_checks={boundary_fold_overlaps}")
print(f"fizz_equation_ground_checks={checked_fizz}")
print("guard_coverage_disjointness_and_descent=PASS")
print("proof_local_operational_bridge_scan=PASS")
