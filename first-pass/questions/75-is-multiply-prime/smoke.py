def is_multiply_prime(a):
    count = 0
    i = 2
    while i <= a:
        if a % i == 0:
            count = count + 1
            a = a // i
        else:
            i = i + 1
    return count == 3
assert is_multiply_prime(30) == True
assert is_multiply_prime(8) == True
assert is_multiply_prime(10) == False
assert is_multiply_prime(5) == False
assert is_multiply_prime(60) == False
