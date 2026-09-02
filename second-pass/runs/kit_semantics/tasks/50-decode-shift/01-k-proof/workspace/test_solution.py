from itertools import product

from prompt import encode_shift
from solution import decode_shift


alphabet = "abcdefghijklmnopqrstuvwxyz"
checked = 0

for length in range(4):
    for chars in product(alphabet, repeat=length):
        original = "".join(chars)
        encoded = encode_shift(original)
        assert decode_shift(encoded) == original
        checked += 1

print(f"cases={checked} mismatches=0")
