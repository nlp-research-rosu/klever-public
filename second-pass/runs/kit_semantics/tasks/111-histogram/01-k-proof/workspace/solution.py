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
