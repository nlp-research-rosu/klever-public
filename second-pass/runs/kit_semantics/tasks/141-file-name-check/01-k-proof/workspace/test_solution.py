import itertools
import random
import re

from solution import file_name_check


def oracle(file_name):
    shape_is_valid = re.fullmatch(
        r"[A-Za-z][^.]*\.(?:txt|exe|dll)", file_name
    )
    ascii_digit_count = sum("0" <= char <= "9" for char in file_name)
    return "Yes" if shape_is_valid and ascii_digit_count <= 3 else "No"


curated = {
    "",
    ".txt",
    "a.txt",
    "example.txt",
    "1example.dll",
    "abc.exe",
    "Z9.dll",
    "abc",
    "a.b.txt",
    "abc.atxt",
    "a123.txt",
    "a1234.txt",
    "A0b1c2.dll",
    "é.txt",
    "añ.txt",
    "a中.exe",
    "a🙂.dll",
    "abc.TXT",
    "a.exe.",
}

small_alphabet = "aZ09.txedl?"
exhaustive = {
    "".join(chars)
    for length in range(6)
    for chars in itertools.product(small_alphabet, repeat=length)
}

rng = random.Random(20260725)
sample_alphabet = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789._-? é中🙂"
)
random_sample = {
    "".join(rng.choice(sample_alphabet) for _ in range(rng.randrange(21)))
    for _ in range(5000)
}

cases = curated | exhaustive | random_sample
mismatches = []
for case in cases:
    actual = file_name_check(case)
    expected = oracle(case)
    if actual != expected:
        mismatches.append((case, actual, expected))

print(f"checked={len(cases)} mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(repr(mismatch))
assert not mismatches
