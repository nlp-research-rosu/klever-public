def truncate_number(number: float) -> float:
    return number % 1.0


input_value = 5e-324
actual_value = truncate_number(input_value)
expected_value = 5e-324
