def count_nums(arr):
    def digits_sum(n):
        neg = 1
        if n < 0: n, neg = -1 * n, -1
        n = [int(i) for i in str(n)]
        n[0] = n[0] * neg
        return sum(n)
    ds = [digits_sum(i) for i in arr]
    return len([v for v in ds if v > 0])


# Smoke checks — the HumanEval/108 dataset `check` cases (bare-value asserts).
assert count_nums([]) == 0
assert count_nums([-1, 11, -11]) == 1
assert count_nums([1, 1, 2]) == 3
assert count_nums([-123]) == 1
assert count_nums([0, 0, 0]) == 0
assert count_nums([10, -10, 100, -100]) == 2
