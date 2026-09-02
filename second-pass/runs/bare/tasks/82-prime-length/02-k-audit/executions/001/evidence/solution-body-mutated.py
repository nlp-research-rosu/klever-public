def prime_length(string):
    n = len(string)
    return n >= 3 and all(n % i != 0 for i in range(2, n))
