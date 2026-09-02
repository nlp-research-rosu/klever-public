from solution import even_odd_palindrome


def arithmetic_palindrome(value):
    original = value
    reversed_value = 0
    while value:
        reversed_value = reversed_value * 10 + value % 10
        value //= 10
    return original == reversed_value


def independent_oracle(n):
    even = 0
    odd = 0
    for value in range(1, n + 1):
        if arithmetic_palindrome(value):
            if value % 2 == 0:
                even += 1
            else:
                odd += 1
    return even, odd


mismatches = []
for n in range(1, 1001):
    actual = even_odd_palindrome(n)
    expected = independent_oracle(n)
    if actual != expected:
        mismatches.append((n, actual, expected))

print("inputs_checked=1000")
print("mismatches=" + str(len(mismatches)))
assert not mismatches
