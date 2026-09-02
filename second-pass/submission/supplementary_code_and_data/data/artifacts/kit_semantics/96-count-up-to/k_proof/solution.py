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
