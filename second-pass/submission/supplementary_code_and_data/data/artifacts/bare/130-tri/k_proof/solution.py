def tri(n):
    if n == 0:
        return [1]
    if n % 2 == 0:
        return tri(n - 1) + [1 + n // 2]
    return tri(n - 1) + [((n + 1) // 2) * ((n + 5) // 2)]
