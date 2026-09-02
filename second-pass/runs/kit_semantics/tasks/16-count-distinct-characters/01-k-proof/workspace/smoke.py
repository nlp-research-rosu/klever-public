def count_distinct_characters(string: str) -> int:
    return len(set(string.lower()))


empty_result = count_distinct_characters("")
example_one_result = count_distinct_characters("xyzXYZ")
example_two_result = count_distinct_characters("Jerry")
