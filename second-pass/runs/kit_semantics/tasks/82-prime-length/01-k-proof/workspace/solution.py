def prime_length(string):
    """Return whether the length of string is a prime number."""
    n = len(string)
    divisor = 2
    prime = n >= 2
    while divisor < n:
        if n % divisor == 0:
            prime = False
        divisor = divisor + 1
    return prime
