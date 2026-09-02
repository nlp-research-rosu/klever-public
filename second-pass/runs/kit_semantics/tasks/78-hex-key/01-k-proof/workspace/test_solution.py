from itertools import product

from solution import hex_key


HEX_DIGITS = "0123456789ABCDEF"
PRIME_DIGITS = frozenset("2357BD")


def oracle(text):
    total = 0
    for character in text:
        if character in PRIME_DIGITS:
            total = total + 1
    return total


checked = 0
mismatches = []
for length in range(5):
    for characters in product(HEX_DIGITS, repeat=length):
        text = "".join(characters)
        expected = oracle(text)
        actual = hex_key(text)
        checked += 1
        if actual != expected:
            mismatches.append((text, expected, actual))

print(f"checked={checked} mismatches={len(mismatches)}")
assert not mismatches
