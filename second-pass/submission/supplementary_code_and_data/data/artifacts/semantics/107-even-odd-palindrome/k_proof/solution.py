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
