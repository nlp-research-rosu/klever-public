def is_equal_to_sum_even(n):
    return n >= 8 and n % 2 == 0


assert is_equal_to_sum_even(4) == False
assert is_equal_to_sum_even(6) == False
assert is_equal_to_sum_even(8) == True
assert is_equal_to_sum_even(10) == True
assert is_equal_to_sum_even(11) == False
assert is_equal_to_sum_even(-2) == False
