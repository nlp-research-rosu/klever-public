def is_prime(n):
    prime = n >= 2
    k = 0
    for k in range(2, n - 1):
        if n % k == 0:
            prime = False
    return prime
