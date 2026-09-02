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
