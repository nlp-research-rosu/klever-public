def compare(game, guess):
    """Return the absolute error for each corresponding score and guess."""
    result = []
    for score, prediction in zip(game, guess):
        result.append(abs(score - prediction))
    return result


assert compare([1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]) == [0, 0, 0, 0, 3, 3]
assert compare([0, 5, 0, 0, 0, 4], [4, 1, 1, 0, 0, -2]) == [4, 4, 1, 0, 0, 6]
assert compare([], []) == []
assert compare([7], [7]) == [0]
assert compare([9], [2]) == [7]
assert compare([2], [9]) == [7]
assert compare([-7, -9], [-2, -14]) == [5, 5]
