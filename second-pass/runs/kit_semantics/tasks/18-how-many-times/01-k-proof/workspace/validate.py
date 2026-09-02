from itertools import product

from solution import how_many_times


def oracle(string: str, substring: str) -> int:
    width = len(substring)
    return sum(
        string[index:index + width] == substring
        for index in range(len(string) - width + 1)
    )


alphabet = "ab"
strings = [
    "".join(chars)
    for length in range(7)
    for chars in product(alphabet, repeat=length)
]
patterns = [
    "".join(chars)
    for length in range(4)
    for chars in product(alphabet, repeat=length)
]

mismatches = []
for string in strings:
    for substring in patterns:
        actual = how_many_times(string, substring)
        expected = oracle(string, substring)
        if actual != expected:
            mismatches.append((string, substring, actual, expected))

print(f"CASES={len(strings) * len(patterns)}")
print(f"MISMATCHES={len(mismatches)}")
if mismatches:
    print(mismatches[:10])
    raise SystemExit(1)


def build_is(codes: tuple[int, ...], index: int, stop: int) -> tuple[int, ...]:
    result = []
    while index < stop:
        result.append(codes[index])
        index += 1
    return tuple(result)


slice_mismatches = []
slice_cases = 0
for length in range(1, 9):
    for codes in product(range(3), repeat=length):
        slice_cases += 1
        start = 1 if 1 < len(codes) else len(codes)
        fixed_semantics_shape = build_is(codes, start, len(codes))
        python_oracle = codes[1:]
        if fixed_semantics_shape != python_oracle:
            slice_mismatches.append(
                (codes, fixed_semantics_shape, python_oracle)
            )

print(f"SLICE_CASES={slice_cases}")
print(f"SLICE_MISMATCHES={len(slice_mismatches)}")
if slice_mismatches:
    print(slice_mismatches[:10])
    raise SystemExit(1)
