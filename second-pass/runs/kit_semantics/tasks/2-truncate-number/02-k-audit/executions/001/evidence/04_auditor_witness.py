"""Concrete satisfying inputs for the audited truncate_number implementation."""


def truncate_number(number: float) -> float:
    return number % 1.0


assert truncate_number(3.5) == 0.5
assert truncate_number(1.0) == 0.0
assert truncate_number(123.875) == 0.875
