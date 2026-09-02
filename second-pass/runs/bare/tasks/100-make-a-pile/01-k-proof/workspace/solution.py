def make_a_pile(n):
    result = []
    i = n - 1
    while i >= 0:
        result = [n + 2 * i] + result
        i = i - 1
    return result
