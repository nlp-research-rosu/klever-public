from solution import sum_to_n


def oracle(n: int) -> int:
    return sum(range(1, n + 1))


inputs = list(range(-1000, 1001))
mismatches = [
    (n, sum_to_n(n), oracle(n))
    for n in inputs
    if sum_to_n(n) != oracle(n)
]

print(f"inputs={len(inputs)} mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:10])
