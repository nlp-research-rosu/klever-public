def make_a_pile(n):
    stones = []
    i = 0
    while i < n:
        stones.append(n + 2 * i)
        i += 1
    return stones


assert make_a_pile(1) == [1]
assert make_a_pile(3) == [3, 5, 7]
assert make_a_pile(4) == [4, 6, 8, 10]
