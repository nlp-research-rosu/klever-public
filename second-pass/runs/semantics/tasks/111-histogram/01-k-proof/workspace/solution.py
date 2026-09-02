def histogram(test):
    counts = {}
    maximum = 0

    for letter in test.split():
        if letter in counts.keys():
            counts[letter] = counts[letter] + 1
        else:
            counts[letter] = 1

        if counts[letter] > maximum:
            maximum = counts[letter]

    result = {}
    for letter in counts.keys():
        if counts[letter] == maximum:
            result[letter] = counts[letter]

    return result
