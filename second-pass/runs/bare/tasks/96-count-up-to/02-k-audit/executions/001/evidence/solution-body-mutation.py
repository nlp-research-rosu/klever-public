def count_up_to(n):
    primes = []
    candidate = 2
    while candidate < n:
        is_prime = True
        divisor = 2
        while divisor * divisor <= candidate:
            if candidate % divisor == 0:
                is_prime = False
            divisor = divisor + 1
        if is_prime:
            primes = primes + [candidate]
        candidate = candidate + 2
    return primes
