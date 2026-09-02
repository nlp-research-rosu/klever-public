def below_zero(operations):
    balance = 0
    operation = 0
    for operation in operations:
        balance += operation
        if balance < 0:
            return True
    return False


assert below_zero([]) == False
assert below_zero([1, 2, 3]) == False
assert below_zero([1, 2, -4, 5]) == True
assert below_zero([0]) == False
assert below_zero([-1]) == True
assert below_zero([5, -5, -1]) == True
