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


assert f(0) == []
assert f(1) == [1]
assert f(2) == [1, 2]
assert f(3) == [1, 2, 6]
assert f(5) == [1, 2, 6, 24, 15]
assert f(8) == [1, 2, 6, 24, 15, 720, 28, 40320]
