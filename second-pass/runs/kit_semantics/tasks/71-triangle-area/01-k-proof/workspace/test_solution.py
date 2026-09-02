from solution import triangle_area


CASES = [
    ((3, 4, 5), 6.0),
    ((1, 2, 10), -1),
    ((2, 2, 3), 1.98),
    ((2.5, 3.0, 4.0), 3.75),
    ((1, 1, 2), -1),
    ((True, True, True), 0.43),
]


for arguments, expected in CASES:
    actual = triangle_area(*arguments)
    assert actual == expected, (arguments, actual, expected)

print(f"CPython cases passed: {len(CASES)}")
