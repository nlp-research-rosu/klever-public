from itertools import product

from solution import same_chars


def oracle_same_chars(s0, s1):
    for char in s0:
        if char not in s1:
            return False
    for char in s1:
        if char not in s0:
            return False
    return True


prompt_examples = [
    ("eabcdzzzz", "dddzzzzzzzddeddabc", True),
    ("abcd", "dddddddabc", True),
    ("dddddddabc", "abcd", True),
    ("eabcd", "dddddddabc", False),
    ("abcd", "dddddddabce", False),
    ("eabcdzzzz", "dddzzzzzzzddddabc", False),
]

strings = [
    "".join(chars)
    for length in range(5)
    for chars in product("abc", repeat=length)
]

mismatches = []
for s0 in strings:
    for s1 in strings:
        expected = oracle_same_chars(s0, s1)
        actual = same_chars(s0, s1)
        if actual != expected:
            mismatches.append((s0, s1, expected, actual))

for s0, s1, expected in prompt_examples:
    actual = same_chars(s0, s1)
    if actual != expected:
        mismatches.append((s0, s1, expected, actual))

print(
    "prompt_examples={0} exhaustive_pairs={1} mismatches={2}".format(
        len(prompt_examples),
        len(strings) * len(strings),
        len(mismatches),
    )
)
if mismatches:
    raise AssertionError(mismatches[:10])
