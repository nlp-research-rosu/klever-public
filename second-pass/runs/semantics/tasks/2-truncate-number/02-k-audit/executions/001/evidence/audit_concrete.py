def truncate_number(number: float) -> float:
    return number % 1.0


# Documented example, exact integers, values below/above integer boundaries,
# and representative small/large positive finite inputs.
assert truncate_number(3.5) == 0.5
assert truncate_number(1.0) == 0.0
assert truncate_number(0.25) == 0.25
assert truncate_number(7.75) == 0.75
assert truncate_number(10.125) == 0.125
assert truncate_number(1024.5) == 0.5
