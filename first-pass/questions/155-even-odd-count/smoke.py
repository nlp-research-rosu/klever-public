def even_odd_count(num):
    even_count = 0
    odd_count = 0
    for i in str(abs(num)):
        if int(i) % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    return (even_count, odd_count)


# Smoke checks from the prompt docstring (NOT hidden tests).
assert even_odd_count(-12) == (1, 1)
assert even_odd_count(123) == (1, 2)
assert even_odd_count(0) == (1, 0)
assert even_odd_count(2468) == (4, 0)
