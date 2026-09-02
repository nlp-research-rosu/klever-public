def compare(game, guess):
    return [abs(x - y) for x, y in zip(game, guess)]


# HumanEval/152 test cases (the dataset `check`); returns a list.
assert compare([1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]) == [0, 0, 0, 0, 3, 3]
assert compare([0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]) == [0, 0, 0, 0, 0, 0]
assert compare([1, 2, 3], [-1, -2, -3]) == [2, 4, 6]
assert compare([1, 2, 3, 5], [-1, 2, 3, 4]) == [2, 0, 0, 1]
