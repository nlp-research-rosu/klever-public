def truncate_number(number: float) -> float:
    return number % 1.0


observed = truncate_number(5e-324)
expected = 5e-324
