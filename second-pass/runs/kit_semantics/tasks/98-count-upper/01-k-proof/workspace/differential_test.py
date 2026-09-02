from itertools import product

from solution import count_upper


def oracle(s):
    return sum(
        1
        for index, char in enumerate(s)
        if index % 2 == 0 and char in "AEIOU"
    )


alphabet = "AEIOUaeiouZ"
cases = [
    "".join(chars)
    for length in range(6)
    for chars in product(alphabet, repeat=length)
]
cases.extend(["aBCdEf", "abcdefg", "dBBE", "ÅE🙂I", "🙂A🙂E"])

mismatches = [
    (value, count_upper(value), oracle(value))
    for value in cases
    if count_upper(value) != oracle(value)
]

print("cases=" + str(len(cases)))
print("mismatches=" + str(len(mismatches)))
if mismatches:
    raise AssertionError(mismatches[:10])
