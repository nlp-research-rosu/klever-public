def fruit_distribution(s, n):
    return n - int(s.split()[0]) - int(s.split()[3])


assert fruit_distribution("5 apples and 6 oranges", 19) == 8
assert fruit_distribution("0 apples and 1 oranges", 3) == 2
assert fruit_distribution("2 apples and 3 oranges", 100) == 95
assert fruit_distribution("100 apples and 1 oranges", 120) == 19
assert fruit_distribution("0 apples and 0 oranges", 0) == 0
assert fruit_distribution("7 apples and 8 oranges", 15) == 0
assert fruit_distribution("  7   apples\tand  8 oranges\n", 20) == 5
assert fruit_distribution("999999 apples and 1 oranges", 1000000) == 0
