def prime_length(string):
    n = len(string)
    if n < 2:
        return False

    divisor = 2
    while divisor < n:
        if n % divisor == 0:
            return False
        divisor += 1

    return True


assert prime_length("Hello") == True
assert prime_length("abcdcba") == True
assert prime_length("kittens") == True
assert prime_length("orange") == False
assert prime_length("") == False
assert prime_length("a") == False
assert prime_length("aa") == True
assert prime_length("aaa") == True
assert prime_length("aaaa") == False
assert prime_length("aaaaa") == True
assert prime_length("aaaaaa") == False
assert prime_length("aaaaaaa") == True
assert prime_length("aaaaaaaa") == False
assert prime_length("aaaaaaaaa") == False
assert prime_length("aaaaaaaaaaa") == True
assert prime_length("aaaaaaaaaaaa") == False
