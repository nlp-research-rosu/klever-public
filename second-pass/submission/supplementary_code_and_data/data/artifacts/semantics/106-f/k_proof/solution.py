def f(n):
    result = []
    factorial = 1
    total = 0
    i = 1
    while i <= n:
        factorial *= i
        total += i
        if i % 2 == 0:
            result.append(factorial)
        else:
            result.append(total)
        i += 1
    return result
