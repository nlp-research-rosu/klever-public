def histogram(test):
    letters = test.split()
    counts = {}
    maximum = 0

    for letter in letters:
        if letter in counts:
            counts[letter] = counts[letter] + 1
        else:
            counts[letter] = 1

        if counts[letter] > maximum:
            maximum = counts[letter]

    result = {}
    for letter in counts:
        if counts[letter] == maximum:
            result[letter] = counts[letter]

    return result
