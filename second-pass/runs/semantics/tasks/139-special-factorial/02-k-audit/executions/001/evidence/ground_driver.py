def special_factorial(n):
    factorial = 1
    result = 1
    i = 1
    while i <= n:
        factorial *= i
        result *= factorial
        i += 1
    return result


answer_n1 = special_factorial(1)
answer_n2 = special_factorial(2)
answer_n4 = special_factorial(4)
answer_n6 = special_factorial(6)
