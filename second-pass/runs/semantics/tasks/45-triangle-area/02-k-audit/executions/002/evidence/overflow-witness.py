def triangle_area(a, h):
    return a * h / 2


# CPython evaluates this submitted function call to 1e308. The supplied
# semantics' divII concrete equation first converts the 2e308 numerator to a
# binary64 value, exposing whether the trusted primitive matches CPython.
assert triangle_area(10 ** 308, 2) == 1e308
