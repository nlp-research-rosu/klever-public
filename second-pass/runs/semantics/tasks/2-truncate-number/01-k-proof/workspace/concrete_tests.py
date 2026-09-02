def truncate_number(number: float) -> float:
    return number % 1.0


assert truncate_number(3.5) == 0.5
assert truncate_number(1.0) == 0.0
assert truncate_number(0.25) == 0.25
assert truncate_number(7.75) == 0.75
