#!/usr/bin/env python3
"""Generate independent ground checks for every proof-local value function."""


def scan_expected(seen: bool, number: int, divisor: int) -> bool:
    if seen:
        return True
    divisor = max(divisor, 2)
    return any(number % item == 0 for item in range(divisor, number))


def bool_token(value: bool) -> str:
    return "true" if value else "false"


scan_cases = []
for number in (-3, 0, 1, 2, 3, 4, 5, 6, 9, 25, 29, 35, 97):
    for divisor in (-2, 2, 3, max(2, number - 1), max(2, number), number + 1):
        scan_cases.append((False, number, divisor))
for number, divisor in ((-3, -2), (2, 2), (35, 8), (97, 96)):
    scan_cases.append((True, number, divisor))

prime_cases = (-5, 0, 1, 2, 3, 4, 5, 9, 25, 29, 97)
overlap_cases = [
    (0, 2, 0, 2),
    (0, 1, 3, 4),
    (-3, -1, -5, 5),
    (-101, -4, -200, 100),
]

print("Module(")
for seen, number, divisor in scan_cases:
    expected = bool_token(scan_expected(seen, number, divisor))
    print(
        "  Assert(Compare("
        f"scanHasDivisor({bool_token(seen)}, {number}, {divisor}), "
        f'CmpOp("==", Bool({expected}))))'
    )
for number in prime_cases:
    prime = number >= 2 and not any(number % item == 0 for item in range(2, number))
    expected_codes = '"YES"' if prime else '"NO"'
    print(
        "  Assert(Compare("
        f"primeResult({number}), "
        f'CmpOp("==", Str({expected_codes}))))'
    )
for a0, a1, b0, b1 in overlap_cases:
    expected = min(a1, b1) - max(a0, b0)
    print(
        "  Assert(Compare("
        f"overlapLength({a0}, {a1}, {b0}, {b1}), "
        f'CmpOp("==", Int({expected}))))'
    )
print(")")
print(
    f"// scan_cases={len(scan_cases)} prime_cases={len(prime_cases)} "
    f"overlap_cases={len(overlap_cases)}"
)
