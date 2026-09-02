def even_odd_count(num):
    if num < 0:
        num = -num
    even = 0
    odd = 0
    while num > 0:
        if num % 2 == 0:
            even += 1
        else:
            odd += 1
        num = num // 10
    return (even, odd)
