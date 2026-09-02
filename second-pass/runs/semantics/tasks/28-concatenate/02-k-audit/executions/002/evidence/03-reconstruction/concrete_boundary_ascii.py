from typing import List


def concatenate(strings: List[str]) -> str:
    result = ""
    string = ""
    for string in strings:
        result += string
    return result


assert concatenate([]) == ""
assert concatenate([""]) == ""
assert concatenate(["x"]) == "x"
assert concatenate(["", "a", "", "b", ""]) == "ab"
assert concatenate(["hello", " ", "world"]) == "hello world"
assert concatenate(["line1\n", "line2"]) == "line1\nline2"
