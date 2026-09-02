from itertools import product

from solution import filter_by_prefix


def oracle(strings, prefix):
    # Independent characterization: compare the slice of prefix length.
    return [s for s in strings if s[: len(prefix)] == prefix]


alphabet = "ab"
words = [""]
for length in range(1, 4):
    words.extend("".join(chars) for chars in product(alphabet, repeat=length))

prefixes = words + ["c", "é", "🙂"]
test_lists = [[]]
for length in range(1, 3):
    test_lists.extend([*items] for items in product(words, repeat=length))
test_lists.extend(
    [
        ["éclair", "eclair", "élan", ""],
        ["🙂a", "🙂", "a🙂", ""],
        ["same", "same", "different"],
    ]
)

cases = 0
mismatches = 0
for strings in test_lists:
    for prefix in prefixes:
        cases += 1
        actual = filter_by_prefix(strings, prefix)
        expected = oracle(strings, prefix)
        if actual != expected:
            mismatches += 1
            print(
                "mismatch:",
                {"strings": strings, "prefix": prefix},
                actual,
                expected,
            )

print(f"differential cases: {cases}; mismatches: {mismatches}")
if mismatches:
    raise SystemExit(1)
