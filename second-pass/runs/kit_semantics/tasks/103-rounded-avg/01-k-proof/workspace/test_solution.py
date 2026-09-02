from solution import rounded_avg


examples = [
    (1, 5, "0b11"),
    (7, 5, -1),
    (10, 20, "0b1111"),
    (20, 33, "0b11010"),
]

for n, m, expected in examples:
    assert rounded_avg(n, m) == expected

checked = 0
for n in range(1, 101):
    for m in range(1, 101):
        if n > m:
            expected = -1
        else:
            values = range(n, m + 1)
            expected = bin(round(sum(values) / len(values)))
        assert rounded_avg(n, m) == expected
        checked += 1

print(f"CPython examples: {len(examples)}/{len(examples)}")
print(f"Independent differential grid: {checked}/{checked}; mismatches: 0")
