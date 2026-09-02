def truncate_number(number: float) -> float:
    return number % 1.0


assert truncate_number(1.0000000000000002) == 2.220446049250313e-16
