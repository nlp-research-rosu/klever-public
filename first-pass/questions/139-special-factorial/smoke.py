def special_factorial(n):
    fact_i = 1
    special_fact = 1
    for i in range(1, n + 1):
        fact_i *= i
        special_fact *= fact_i
    return special_fact


# Smoke checks from the prompt docstring (NOT hidden tests).
assert special_factorial(4) == 288
