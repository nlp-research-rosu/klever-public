def triangle_area(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return -1
    s = (a + b + c) / 2
    return round((s * (s - a) * (s - b) * (s - c)) ** 0.5, 2)


# One satisfiable ground witness for each call-claim precondition.
assert triangle_area(1, 1, 3) == -1  # first inequality
assert triangle_area(1, 3, 1) == -1  # second inequality, first false
assert triangle_area(3, 1, 1) == -1  # third inequality, first two false
assert triangle_area(3, 4, 5) == 6.0  # all three strict inequalities

# Source-contract witness excluded by every formal claim (`Float`, not `Int`).
assert triangle_area(5.5, 6.25, 7.75) == 17.03
