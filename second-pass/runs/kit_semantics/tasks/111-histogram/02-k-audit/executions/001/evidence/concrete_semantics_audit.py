def histogram(test):
    result = {}
    max_count = 0
    letter = ""
    candidate = ""
    count = 0
    phase = 1

    for letter in test:
        if letter != " ":
            count = 0
            for candidate in test:
                if candidate == letter:
                    count = count + 1
            if count > max_count:
                max_count = count

    phase = 2
    for letter in test:
        if letter != " ":
            count = 0
            for candidate in test:
                if candidate == letter:
                    count = count + 1
            if count == max_count:
                result[letter] = count

    return result


# Documented, empty, alphabet-boundary, unique-maximum, tied-maximum,
# skipped-space, and repeated-update cases.
assert histogram("") == {}
assert histogram(" ") == {}
assert histogram("a") == {"a": 1}
assert histogram("z") == {"z": 1}
assert histogram("a b c") == {"a": 1, "b": 1, "c": 1}
assert histogram("a b b a") == {"a": 2, "b": 2}
assert histogram("b b b b a") == {"b": 4}
assert histogram("a z z a") == {"a": 2, "z": 2}
assert histogram("a a b c") == {"a": 2}
assert histogram("a  b") == {"a": 1, "b": 1}
assert histogram("ab") == {"a": 1, "b": 1}
