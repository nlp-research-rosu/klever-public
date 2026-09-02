def count_distinct_characters(string: str) -> int:
    return len(set(string.lower()))


assert count_distinct_characters("") == 0
assert count_distinct_characters("xyzXYZ") == 3
assert count_distinct_characters("Jerry") == 4
assert count_distinct_characters("AaBbCcAa") == 3
assert count_distinct_characters("123!123!") == 4
