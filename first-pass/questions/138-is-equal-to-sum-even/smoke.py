def is_equal_to_sum_even(n):
    return n % 2 == 0 and n >= 8


# HumanEval/138 test cases (the dataset `check`); returns a bool.
assert not is_equal_to_sum_even(4)
assert not is_equal_to_sum_even(6)
assert is_equal_to_sum_even(8)
assert is_equal_to_sum_even(10)
assert not is_equal_to_sum_even(11)
assert is_equal_to_sum_even(12)
assert not is_equal_to_sum_even(13)
assert is_equal_to_sum_even(16)
