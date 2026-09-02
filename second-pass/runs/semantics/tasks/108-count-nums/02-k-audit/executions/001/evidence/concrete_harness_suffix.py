

assert positive_digit_sum(0) == 0
assert positive_digit_sum(1) == 1
assert positive_digit_sum(9) == 9
assert positive_digit_sum(10) == 1
assert positive_digit_sum(999) == 27

assert negative_digit_sum(0) == 0
assert negative_digit_sum(9) == -9
assert negative_digit_sum(10) == -1
assert negative_digit_sum(11) == 0
assert negative_digit_sum(12) == 1
assert negative_digit_sum(100) == -1

assert signed_digit_sum(-12) == 1
assert signed_digit_sum(-11) == 0
assert signed_digit_sum(-1) == -1
assert signed_digit_sum(0) == 0
assert signed_digit_sum(10) == 1

assert count_nums([]) == 0
assert count_nums([-1, 11, -11]) == 1
assert count_nums([1, 1, 2]) == 3
assert count_nums([-9, -10, -11, -12, 0, 9, 10, 11]) == 4
assert count_nums([0, 10, -10, 123, -123]) == 3
assert count_nums([-12, -21, -123, -999, 100, -100]) == 4
