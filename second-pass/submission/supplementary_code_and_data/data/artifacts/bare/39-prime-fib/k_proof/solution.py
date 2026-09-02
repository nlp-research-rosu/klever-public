def prime_fib(n: int):
    a = 0
    b = 1
    count = 0
    while count < n:
        c = a + b
        a = b
        b = c
        divisor = 2
        prime = True
        if b < 2:
            prime = False
        while divisor * divisor <= b:
            if b % divisor == 0:
                prime = False
            divisor = divisor + 1
        if prime:
            count = count + 1
    return b
