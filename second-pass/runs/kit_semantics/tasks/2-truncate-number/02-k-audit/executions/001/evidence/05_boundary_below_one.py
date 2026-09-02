def truncate_number(number: float) -> float:
    return number % 1.0


assert truncate_number(0.9999999999999999) == 0.9999999999999999
