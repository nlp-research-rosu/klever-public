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


assert prime_length("") == False
assert prime_length("a") == False
assert prime_length("ab") == True
assert prime_length("abc") == True
assert prime_length("abcd") == False
assert prime_length("abcde") == True
assert prime_length("abcdef") == False
assert prime_length("abcdefg") == True
assert prime_length("abcdefgh") == False
assert prime_length("abcdefghi") == False
assert prime_length("abcdefghij") == False
assert prime_length("abcdefghijk") == True
assert prime_length("abcdefghijkl") == False
assert prime_length("abcdefghijklm") == True
assert prime_length("abcdefghijklmn") == False
assert prime_length("abcdefghijklmno") == False
