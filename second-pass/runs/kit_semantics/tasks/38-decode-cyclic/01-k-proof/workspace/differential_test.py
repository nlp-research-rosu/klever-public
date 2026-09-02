from itertools import product

from prompt import encode_cyclic
from solution import decode_cyclic


alphabet = "aB0!"
tested = 0
mismatches = []

for length in range(9):
    for chars in product(alphabet, repeat=length):
        original = "".join(chars)
        encoded = encode_cyclic(original)
        actual = decode_cyclic(encoded)
        tested += 1
        if actual != original:
            mismatches.append((original, encoded, actual))

unicode_cases = [
    "é",
    "λ🙂",
    "日本語",
    "a\u0301bc",
    "🙂🙃😉😊x",
    "𝄞music",
]

for original in unicode_cases:
    encoded = encode_cyclic(original)
    actual = decode_cyclic(encoded)
    tested += 1
    if actual != original:
        mismatches.append((original, encoded, actual))

print(f"cases={tested}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)
