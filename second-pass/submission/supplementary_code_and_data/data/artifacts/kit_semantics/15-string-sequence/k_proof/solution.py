def string_sequence(n: int) -> str:
    """Return space-delimited integers from 0 through n, inclusive."""
    if n < 0:
        return ""

    result = "0"
    i = 1
    while i <= n:
        result = result + " " + str(i)
        i = i + 1
    return result
