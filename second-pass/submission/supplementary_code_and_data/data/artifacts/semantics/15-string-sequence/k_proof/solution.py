def string_sequence(n: int) -> str:
    """Return the decimal integers from 0 through n, separated by spaces."""
    if n < 0:
        return ""
    result = "0"
    i = 1
    for i in range(1, n + 1):
        result = result + (" " + str(i))
    return result
