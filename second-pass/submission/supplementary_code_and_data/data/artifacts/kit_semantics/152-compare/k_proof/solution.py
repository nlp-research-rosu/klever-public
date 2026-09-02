def compare(game, guess):
    result = []
    for score, predicted in zip(game, guess):
        result.append(abs(score - predicted))
    return result
