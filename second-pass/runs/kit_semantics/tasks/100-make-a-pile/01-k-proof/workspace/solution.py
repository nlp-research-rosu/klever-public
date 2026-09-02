def make_a_pile(n):
    pile = []
    i = 0
    while i < n:
        pile.append(n + 2 * i)
        i += 1
    return pile
