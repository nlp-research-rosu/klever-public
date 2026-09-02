def compare(game, guess):
    """Return the absolute error for each corresponding score and guess."""
    result = []
    for score, prediction in zip(game, guess):
        result.append(abs(score - prediction))
    return result


assert compare([1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]) == [0, 0, 0, 0, 3, 3]
assert compare([0, 5, 0, 0, 0, 4], [4, 1, 1, 0, 0, -2]) == [4, 4, 1, 0, 0, 6]
assert compare([], []) == []
assert compare([0], [0]) == [0]
assert compare([2], [-1]) == [3]
assert compare([-2], [1]) == [3]
assert compare([-7, 9], [5, -4]) == [12, 13]
assert compare([1], [4, 5]) == [3]
assert compare([1, 2], [4]) == [3]
