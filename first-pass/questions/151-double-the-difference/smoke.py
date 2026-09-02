def double_the_difference(lst):
    result = 0
    e = 0
    for e in lst:
        if e > 0:
            if e % 2 == 1:
                result = result + e * e
    return result


# HumanEval/151 test cases (the integer dataset `check` cases; the float cases
# 0.1/0.2/0.3 are outside the modeled List[int] domain — see PROOF.md).
assert double_the_difference([1, 3, 2, 0]) == 10
assert double_the_difference([-1, -2, 0]) == 0
assert double_the_difference([9, -2]) == 81
assert double_the_difference([0]) == 0
assert double_the_difference([5, 4]) == 25
assert double_the_difference([-10, -20, -30]) == 0
assert double_the_difference([-1, -2, 8]) == 0
