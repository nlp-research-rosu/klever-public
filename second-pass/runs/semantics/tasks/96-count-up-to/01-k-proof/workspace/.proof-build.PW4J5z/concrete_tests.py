def count_up_to(n):
    result = []
    candidate = 2
    is_prime = True
    divisor = 2
    while candidate < n:
        while divisor < candidate:
            if candidate % divisor == 0:
                is_prime = False
            divisor += 1
        if is_prime:
            result.append(candidate)
        candidate += 1
        is_prime = True
        divisor = 2
    return result
assert count_up_to(5) == [2, 3]
assert count_up_to(11) == [2, 3, 5, 7]
assert count_up_to(0) == []
assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
assert count_up_to(1) == []
assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]
