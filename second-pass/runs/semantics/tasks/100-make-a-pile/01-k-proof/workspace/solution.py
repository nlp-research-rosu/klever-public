def make_a_pile(n):
    stones = []
    i = 0
    while i < n:
        stones.append(n + 2 * i)
        i += 1
    return stones
