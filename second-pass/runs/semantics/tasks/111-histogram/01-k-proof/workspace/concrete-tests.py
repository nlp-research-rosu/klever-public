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


assert histogram("a b c") == {"a": 1, "b": 1, "c": 1}
assert histogram("a b b a") == {"a": 2, "b": 2}
assert histogram("a b c a b") == {"a": 2, "b": 2}
assert histogram("b b b b a") == {"b": 4}
assert histogram("") == {}
