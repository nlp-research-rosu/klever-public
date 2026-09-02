# solution.py — canonical verbatim minus the docstring (one function; the
# `or` short-circuit and the float chain run through the shared semantics).


def triangle_area(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return -1
    s = (a + b + c)/2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    area = round(area, 2)
    return area


assert triangle_area(1, 2, 10) == -1
assert triangle_area(1, 2, 3) == -1
assert triangle_area(2, 6, 3) == -1
assert triangle_area(2, 2, 10) == -1
assert triangle_area(10, 1, 1) == -1
assert triangle_area(3, 4, 5) == 6.0
assert triangle_area(5, 12, 13) == 30.0
