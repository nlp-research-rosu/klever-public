def triangle_area(a, h):
    return a * h / 2.0


assert triangle_area(0.1, 0.2) == 0.010000000000000002
assert triangle_area(0.3, 0.7) == 0.105
assert triangle_area(1.1, 3.3) == 1.815
assert triangle_area(1e100, 1e-100) == 0.5
assert triangle_area(2**53 + 1, 1.0) == 4503599627370496.0
assert triangle_area(2**1023, 1) == 4.49423283715579e307
