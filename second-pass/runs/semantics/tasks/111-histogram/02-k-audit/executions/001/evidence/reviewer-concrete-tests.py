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


assert histogram("") == {}
assert histogram("z") == {"z": 1}
assert histogram("z z") == {"z": 2}
assert histogram("z y") == {"z": 1, "y": 1}
assert histogram("z z y") == {"z": 2}
assert histogram("z y z") == {"z": 2}
assert histogram("z y y") == {"y": 2}
assert histogram("z y x") == {"z": 1, "y": 1, "x": 1}
assert histogram("a a b b c") == {"a": 2, "b": 2}
