def compare(game, guess):
    """Return the absolute error for each corresponding score and guess."""
    result = []
    for score, prediction in zip(game, guess):
        result.append(abs(score - prediction))
    return result
