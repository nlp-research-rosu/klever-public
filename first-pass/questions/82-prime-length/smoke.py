def prime_length(string):
    l = len(string)
    prime = l >= 2
    i = 0
    for i in range(2, l):
        if l % i == 0:
            prime = False
    return prime


# HumanEval/82 dataset `check` cases (bare-bool asserts).
assert prime_length('Hello')
assert prime_length('abcdcba')
assert prime_length('kittens')
assert not prime_length('orange')
assert prime_length('wow')
assert prime_length('world')
assert prime_length('MadaM')
assert prime_length('Wow')
assert not prime_length('')
assert prime_length('HI')
