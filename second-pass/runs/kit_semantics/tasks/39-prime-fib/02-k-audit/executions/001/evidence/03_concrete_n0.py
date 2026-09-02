def prime_fib(n: int):
    a = 0
    b = 1
    count = 0
    next_value = 0
    divisor = 2
    is_prime = False
    while count < n:
        next_value = a + b
        a = b
        b = next_value
        divisor = 2
        is_prime = a >= 2
        while divisor * divisor <= a:
            if a % divisor == 0:
                is_prime = False
            divisor = divisor + 1
        count = count + is_prime
    return a


result = prime_fib(0)
