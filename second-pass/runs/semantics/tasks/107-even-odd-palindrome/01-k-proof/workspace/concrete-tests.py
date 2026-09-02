def even_odd_palindrome(n):
    if n < 10:
        return (n // 2, (n + 1) // 2)

    if n < 100:
        two_digit = n // 11
        return (4 + two_digit // 2, 5 + (two_digit + 1) // 2)

    if n == 1000:
        return (48, 60)

    hundreds = n // 100
    current_block = (n % 100 - hundreds) // 10 + 1
    even = 8 + 10 * ((hundreds - 1) // 2)
    odd = 10 + 10 * (hundreds // 2)

    if hundreds % 2 == 0:
        even += current_block
    else:
        odd += current_block

    return (even, odd)


assert even_odd_palindrome(1) == (0, 1)
assert even_odd_palindrome(3) == (1, 2)
assert even_odd_palindrome(9) == (4, 5)
assert even_odd_palindrome(10) == (4, 5)
assert even_odd_palindrome(12) == (4, 6)
assert even_odd_palindrome(99) == (8, 10)
assert even_odd_palindrome(100) == (8, 10)
assert even_odd_palindrome(111) == (8, 12)
assert even_odd_palindrome(222) == (11, 20)
assert even_odd_palindrome(999) == (48, 60)
assert even_odd_palindrome(1000) == (48, 60)
