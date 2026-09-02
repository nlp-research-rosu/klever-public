from itertools import product

from solution import compare


def oracle(game, guess):
    expected = []
    for index in range(len(game)):
        difference = game[index] - guess[index]
        if difference < 0:
            difference = -difference
        expected.append(difference)
    return expected


values = range(-3, 4)
checked = 0
for length in range(4):
    sequences = list(product(values, repeat=length))
    for game in sequences:
        for guess in sequences:
            actual = compare(list(game), list(guess))
            expected = oracle(game, guess)
            assert actual == expected, (game, guess, actual, expected)
            checked += 1

print(f"DIFFERENTIAL_TESTS_PASS={checked}")
