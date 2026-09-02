def generate_integers(a, b):
    result = []
    if (a <= 2 and 2 <= b) or (b <= 2 and 2 <= a):
        result.append(2)
    if (a <= 4 and 4 <= b) or (b <= 4 and 4 <= a):
        result.append(4)
    if (a <= 6 and 6 <= b) or (b <= 6 and 6 <= a):
        result.append(6)
    if (a <= 8 and 8 <= b) or (b <= 8 and 8 <= a):
        result.append(8)
    return result


assert generate_integers(2, 8) == [2, 4, 6, 8]
assert generate_integers(8, 2) == [2, 4, 6, 8]
assert generate_integers(10, 14) == []
assert generate_integers(1, 1) == []
assert generate_integers(2, 2) == [2]
assert generate_integers(3, 4) == [4]
assert generate_integers(5, 6) == [6]
assert generate_integers(7, 8) == [8]
assert generate_integers(1, 9) == [2, 4, 6, 8]
assert generate_integers(9, 1) == [2, 4, 6, 8]
