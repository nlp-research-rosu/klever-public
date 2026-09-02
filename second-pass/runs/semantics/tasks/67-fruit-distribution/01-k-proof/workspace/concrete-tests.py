def fruit_distribution(s, n):
    fruits = s.split()
    return n - int(fruits[0]) - int(fruits[3])


assert fruit_distribution("5 apples and 6 oranges", 19) == 8
assert fruit_distribution("0 apples and 1 oranges", 3) == 2
assert fruit_distribution("2 apples and 3 oranges", 100) == 95
assert fruit_distribution("100 apples and 1 oranges", 120) == 19
assert fruit_distribution("12 apples and 34 oranges", 100) == 54
