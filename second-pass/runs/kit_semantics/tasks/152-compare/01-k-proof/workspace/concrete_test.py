def compare(game, guess):
    result = []
    for score, predicted in zip(game, guess):
        result.append(abs(score - predicted))
    return result


assert compare([1, 2, 3, 4, 5, 1], [1, 2, 3, 4, 2, -2]) == [0, 0, 0, 0, 3, 3]
assert compare([0, 5, 0, 0, 0, 4], [4, 1, 1, 0, 0, -2]) == [4, 4, 1, 0, 0, 6]
assert compare([], []) == []
