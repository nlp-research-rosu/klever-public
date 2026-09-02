from decimal import Decimal, ROUND_HALF_UP
import random

from solution import closest_integer


def oracle(text):
    parsed = float(text)
    exact_binary_value = Decimal.from_float(parsed)
    return int(exact_binary_value.to_integral_value(rounding=ROUND_HALF_UP))


cases = [
    "10",
    "15.3",
    "14.5",
    "-14.5",
    "0",
    "0.49",
    "-0.49",
    "0.5",
    "-0.5",
    "2.499",
    "-2.499",
    "2.501",
    "-2.501",
    "9007199254740993",
    "-9007199254740993",
    "0.49999999999999994",
    "0.49999999999999999",
    "-0.49999999999999994",
    "-0.49999999999999999",
]

rng = random.Random(137)
for _ in range(5000):
    sign = "-" if rng.randrange(2) else ""
    integer = str(rng.randrange(10**15))
    fraction_length = rng.randrange(1, 18)
    fraction = "".join(str(rng.randrange(10)) for _ in range(fraction_length))
    cases.append(sign + integer + "." + fraction)

mismatches = []
for text in cases:
    actual = closest_integer(text)
    expected = oracle(text)
    if actual != expected:
        mismatches.append((text, actual, expected))

assert not mismatches, mismatches[:10]
print(f"Differential cases: {len(cases)}; mismatches: {len(mismatches)}")
