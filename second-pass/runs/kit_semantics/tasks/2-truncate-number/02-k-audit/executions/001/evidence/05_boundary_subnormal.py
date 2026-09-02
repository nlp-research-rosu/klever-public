def truncate_number(number: float) -> float:
    return number % 1.0


assert truncate_number(5e-324) == 5e-324
