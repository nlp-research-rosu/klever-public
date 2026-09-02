def compare(game, guess):
    if game == []:
        return []
    difference = game[0] - guess[0]
    if difference < 0:
        difference = -difference
    return [difference] + compare(game[1:], guess[1:])
