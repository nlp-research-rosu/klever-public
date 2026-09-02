def count_up_to(n):
    if n <= 2:
        return []

    primes = []
    candidate = 2
    divisor = 2
    prime = True

    while candidate < n:
        divisor = 2
        prime = True

        while divisor < candidate:
            if candidate % divisor == 0:
                prime = False
            divisor = divisor + 1

        if prime:
            primes.append(candidate)
        candidate = candidate + 1

    return primes


assert count_up_to(5) == [2, 3]
assert count_up_to(11) == [2, 3, 5, 7]
assert count_up_to(0) == []
assert count_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]
assert count_up_to(1) == []
assert count_up_to(18) == [2, 3, 5, 7, 11, 13, 17]
