# solution.py — canonical verbatim minus the docstring (one function; the
# `or` short-circuit and the float chain run through the shared semantics).


def triangle_area(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return -1
    s = (a + b + c)/2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    area = round(area, 2)
    return area
