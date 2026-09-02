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


assert string_sequence(-2) == ""
assert string_sequence(0) == "0"
assert string_sequence(5) == "0 1 2 3 4 5"
assert string_sequence(12) == "0 1 2 3 4 5 6 7 8 9 10 11 12"
