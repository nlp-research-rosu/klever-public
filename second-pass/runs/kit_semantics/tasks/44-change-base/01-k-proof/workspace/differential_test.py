from solution import change_base


def oracle_change_base(x: int, base: int) -> str:
    """Independent most-significant-place conversion oracle."""
    if x == 0:
        return "0"

    sign = "-" if x < 0 else ""
    magnitude = abs(x)
    place = 1
    while place * base <= magnitude:
        place *= base

    digits = []
    while place > 0:
        digit = magnitude // place
        digits.append(chr(48 + digit))
        magnitude %= place
        place //= base
    return sign + "".join(digits)


mismatches = []
for base in range(2, 10):
    for x in range(-250, 251):
        actual = change_base(x, base)
        expected = oracle_change_base(x, base)
        if actual != expected:
            mismatches.append((x, base, actual, expected))

print("domain: x=-250..250, base=2..9")
print(f"cases: {8 * 501}")
print(f"mismatches: {len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
