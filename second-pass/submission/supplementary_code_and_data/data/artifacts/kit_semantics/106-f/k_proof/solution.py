def f(n):
    result = []
    fact = 1
    total = 0
    i = 1
    while i <= n:
        fact *= i
        total += i
        if i % 2 == 0:
            result.append(fact)
        else:
            result.append(total)
        i += 1
    return result
