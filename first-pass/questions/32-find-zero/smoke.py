def find_zero(xs):
    begin = -1.0
    end = 1.0
    center = 0.0
    while poly(xs, begin) * poly(xs, end) > 0.0:
        begin = begin * 2.0
        end = end * 2.0
    while end - begin > 0.0000000001:
        center = (begin + end) / 2.0
        if poly(xs, center) * poly(xs, begin) > 0.0:
            begin = center
        else:
            end = center
    return begin


# Smoke: f(x) = 1 + 2x has root -0.5; bisection converges to within 1e-10. NOT a hidden test.
r = find_zero([1.0, 2.0])
assert r > -0.5000001
assert -0.4999999 > r
