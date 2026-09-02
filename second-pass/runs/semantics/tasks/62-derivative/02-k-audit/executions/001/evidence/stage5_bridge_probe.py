def probe(xs: list):
    result = []
    for i, x in enumerate(xs):
        result.append(i * x)
    result.append(777)
    return result


# The sentinel append is an observable continuation immediately after the
# bridged loop; it detects a bridge that discards or unwinds the suffix.
assert probe([]) == [777]
assert probe([3]) == [0, 777]
assert probe([3, 4]) == [0, 4, 777]
assert probe([3, -4, 5]) == [0, -4, 10, 777]
