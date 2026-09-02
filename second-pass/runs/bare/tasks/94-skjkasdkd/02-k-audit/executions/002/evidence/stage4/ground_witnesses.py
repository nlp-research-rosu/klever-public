#!/usr/bin/env python3
"""Ground witnesses satisfying each formal claim's precondition."""

import importlib.util
import math
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


candidate = load(
    "candidate_ground_witness",
    Path("/tmp/audit-work/candidate-clean/solution.py"),
)
canonical = load("canonical_ground_witness", Path("/reference/canonical.py"))


def ref_prime_from(number, divisor):
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def ref_prime(number):
    return number >= 2 and ref_prime_from(number, 2)


def ref_choose(number, best):
    return number if ref_prime(number) and number > best else best


def ref_largest(values):
    best = 0
    for value in reversed(values):
        best = ref_choose(value, best)
    return best


def ref_digit_sum(number):
    if number < 10:
        return number
    return number % 10 + ref_digit_sum(number // 10)


def ref_answer(values):
    return ref_digit_sum(ref_largest(values))


print("claim1 precondition witness: N=2, D=2 (N>=2 and D>=2)")
print(
    "  candidate is_prime_from(2,2)=",
    candidate.is_prime_from(2, 2),
    "refPrimeFrom(2,2)=",
    ref_prime_from(2, 2),
)

print("claim2 precondition witness: N=1 (no requires clause)")
print(
    "  candidate is_prime(1)=",
    candidate.is_prime(1),
    "refPrime(1)=",
    ref_prime(1),
)

print("claim3 precondition witness: N=7, BEST=5 (no requires clause)")
print(
    "  candidate choose_prime(7,5)=",
    candidate.choose_prime(7, 5),
    "refChoose(7,5)=",
    ref_choose(7, 5),
)

print("claim4 precondition witness: VS=[4,7] (no requires clause)")
print(
    "  candidate largest_prime([4,7])=",
    candidate.largest_prime([4, 7]),
    "refLargest([4,7])=",
    ref_largest([4, 7]),
)

print("claim5 precondition witness: N=181 (no requires clause)")
print(
    "  candidate digit_sum(181)=",
    candidate.digit_sum(181),
    "refDigitSum(181)=",
    ref_digit_sum(181),
)

entry_values = [0, 8, 1, 2, 1, 7]
print(f"claim6 precondition witness: VS={entry_values} (no requires clause)")
print("  refAnswer=", ref_answer(entry_values))
print("  candidate skjkasdkd=", candidate.skjkasdkd(entry_values))
print("  canonical skjkasdkd=", canonical.skjkasdkd(entry_values))

boundary_values = [181, 32, 109]
print(f"additional entry substitution: VS={boundary_values}")
print("  refAnswer=", ref_answer(boundary_values))
print("  candidate skjkasdkd=", candidate.skjkasdkd(boundary_values))
print("  canonical skjkasdkd=", canonical.skjkasdkd(boundary_values))
