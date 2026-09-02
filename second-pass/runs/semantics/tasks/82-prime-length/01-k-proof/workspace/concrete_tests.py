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
assert prime_length("abcdefghijk") == True
assert prime_length("abcdefghijkl") == False
