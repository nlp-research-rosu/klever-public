def string_sequence(n: int) -> str:
    """Return the decimal integers from 0 through n, separated by spaces."""
    if n < 0:
        return ""
    result = "0"
    i = 1
    for i in range(1, n + 1):
        result = result + (" " + str(i))
    return result


assert string_sequence(0) == "0"
assert string_sequence(5) == "0 1 2 3 4 5"
assert string_sequence(10) == "0 1 2 3 4 5 6 7 8 9 10"
