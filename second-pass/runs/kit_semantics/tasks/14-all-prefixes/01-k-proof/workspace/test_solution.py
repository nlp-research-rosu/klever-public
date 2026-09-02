from solution import all_prefixes


def oracle(string: str):
    return [string[:end] for end in range(1, len(string) + 1)]


CASES = [
    "",
    "a",
    "abc",
    "xy",
    "a a",
    "!?",
    "prefix",
    "0123456789",
]


for case in CASES:
    actual = all_prefixes(case)
    expected = oracle(case)
    assert actual == expected, (case, actual, expected)

print(f"CPython oracle cases passed: {len(CASES)}")
