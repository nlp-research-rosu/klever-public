def truncate_number(number):
    return number % 1.0


# Smoke checks from the prompt docstring (NOT hidden tests).
assert truncate_number(3.5) == 0.5
