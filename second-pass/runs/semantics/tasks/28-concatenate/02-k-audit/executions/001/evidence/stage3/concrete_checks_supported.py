from typing import List


def concatenate(strings: List[str]) -> str:
    result = ""
    string = ""
    for string in strings:
        result += string
    return result


assert concatenate([]) == ""
assert concatenate(["x"]) == "x"
assert concatenate(["a", "b", "c"]) == "abc"
assert concatenate(["", "prefix", ""]) == "prefix"
assert concatenate(["é", "中"]) == "é中"
