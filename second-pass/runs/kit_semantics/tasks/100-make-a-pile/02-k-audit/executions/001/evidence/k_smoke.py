def make_a_pile(n):
    pile = []
    i = 0
    while i < n:
        pile.append(n + 2 * i)
        i += 1
    return pile


assert make_a_pile(0) == []
assert make_a_pile(1) == [1]
assert make_a_pile(2) == [2, 4]
assert make_a_pile(3) == [3, 5, 7]
assert make_a_pile(5) == [5, 7, 9, 11, 13]
