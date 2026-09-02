def count_distinct_characters(string):
    return len(set(string.lower()))


# Smoke checks from the prompt docstring (NOT hidden tests).
assert count_distinct_characters('xyzXYZ') == 3
assert count_distinct_characters('Jerry') == 4
