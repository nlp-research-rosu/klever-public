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


assert prime_length("") == False
assert prime_length("a") == False
assert prime_length("ab") == True
assert prime_length("abc") == True
assert prime_length("Hello") == True
assert prime_length("orange") == False
assert prime_length("abcdcba") == True
assert prime_length("kittens") == True
assert prime_length("abcdefghijk") == True
assert prime_length("abcdefghijkl") == False
