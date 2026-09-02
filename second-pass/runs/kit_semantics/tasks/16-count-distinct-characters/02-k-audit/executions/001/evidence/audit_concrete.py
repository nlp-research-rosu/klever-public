def count_distinct_characters(string: str) -> int:
    return len(set(string.lower()))


result_empty = count_distinct_characters("")
result_xyz = count_distinct_characters("xyzXYZ")
result_jerry = count_distinct_characters("Jerry")
result_case_pair = count_distinct_characters("aA")
result_punctuation = count_distinct_characters("a-A_a!A?")
