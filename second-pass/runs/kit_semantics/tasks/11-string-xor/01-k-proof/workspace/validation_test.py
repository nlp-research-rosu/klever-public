from itertools import product

from solution import string_xor


def oracle(a: str, b: str) -> str:
    return "".join(str(int(x) ^ int(y)) for x, y in zip(a, b))


def bit_strings(max_length: int):
    for length in range(max_length + 1):
        for bits in product("01", repeat=length):
            yield "".join(bits)


inputs = list(bit_strings(5))
mismatches = []
for a in inputs:
    for b in inputs:
        actual = string_xor(a, b)
        expected = oracle(a, b)
        if actual != expected:
            mismatches.append((a, b, actual, expected))

print(f"pairs={len(inputs) ** 2} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(mismatch)
    raise SystemExit(1)
