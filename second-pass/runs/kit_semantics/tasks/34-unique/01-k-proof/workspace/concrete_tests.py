from solution import unique


CASES = [
    [],
    [5, 3, 5, 2, 3, 3, 9, 0, 123],
    ["b", "a", "b", "c", "a"],
    [True, 1],
    [True, 1, 0, False, 2],
    [3.0, 2, 2.0, 3],
    [-4, 7, -4, 0, 7, -1],
]


for case in CASES:
    expected = sorted(set(case))
    actual = unique(case)
    assert actual == expected, (case, expected, actual)
    print(f"{case!r} -> {actual!r}")

print(f"CPYTHON_MISMATCHES=0 CASES={len(CASES)}")
