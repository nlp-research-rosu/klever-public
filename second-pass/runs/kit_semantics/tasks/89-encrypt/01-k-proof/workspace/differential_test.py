import random
import string

from solution import encrypt


SOURCE = string.ascii_lowercase
TARGET = SOURCE[4:] + SOURCE[:4]
TABLE = str.maketrans(SOURCE, TARGET)


def oracle(value):
    return value.translate(TABLE)


rng = random.Random(0)
cases = [""]
cases.extend(chr(code) for code in range(128))
cases.extend(
    [
        "abcdefghijklmnopqrstuvwxyz",
        "xyz",
        "a z!",
        "Hello, World!",
        "éclair λ",
    ]
)
alphabet = string.ascii_letters + string.digits + string.punctuation + " "
cases.extend(
    "".join(rng.choice(alphabet) for _ in range(rng.randrange(65)))
    for _ in range(1000)
)

mismatches = [
    (value, encrypt(value), oracle(value))
    for value in cases
    if encrypt(value) != oracle(value)
]

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:5])
