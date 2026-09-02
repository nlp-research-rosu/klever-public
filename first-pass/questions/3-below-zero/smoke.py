def below_zero(operations):
    balance = 0
    for op in operations:
        balance += op
        if balance < 0:
            return True
    return False


# HumanEval/3 test cases (the dataset `check`), using bare-bool asserts.
assert not below_zero([])
assert not below_zero([1, 2, -3, 1, 2, -3])
assert below_zero([1, 2, -4, 5, 6])
assert not below_zero([1, -1, 2, -2, 5, -5, 4, -4])
assert below_zero([1, -1, 2, -2, 5, -5, 4, -5])
assert below_zero([1, -2, 2, -2, 5, -5, 4, -4])
