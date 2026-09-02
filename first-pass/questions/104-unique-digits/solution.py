def unique_digits(x):
    odd_digit_elements = []
    for i in x:
        n = i
        is_odd = True
        while n > 0:
            if n % 10 % 2 == 0:
                is_odd = False
            n = n // 10
        if is_odd:
            odd_digit_elements.append(i)
    return sorted(odd_digit_elements)
