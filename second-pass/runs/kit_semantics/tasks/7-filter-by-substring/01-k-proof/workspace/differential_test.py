from itertools import product

from solution import filter_by_substring


def oracle(strings, substring):
    return list(filter(lambda item: substring in item, strings))


alphabet = "ab"
string_values = [""]
for length in range(1, 3):
    string_values.extend(
        "".join(chars) for chars in product(alphabet, repeat=length)
    )
substrings = string_values + ["c"]

cases = 0
mismatches = 0
for list_length in range(4):
    for items in product(string_values, repeat=list_length):
        strings = list(items)
        for substring in substrings:
            cases += 1
            actual = filter_by_substring(strings, substring)
            expected = oracle(strings, substring)
            if actual != expected:
                mismatches += 1
                print(
                    "mismatch:",
                    repr(strings),
                    repr(substring),
                    repr(actual),
                    repr(expected),
                )

print(f"cases={cases} mismatches={mismatches}")
raise SystemExit(1 if mismatches else 0)
