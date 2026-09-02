from typing import List


def concatenate(strings: List[str]) -> str:
    result = ""
    string = ""
    for string in strings:
        result += string
    return result


assert concatenate([]) == ""
assert concatenate(["a", "b", "c"]) == "abc"
assert concatenate(["hello", "", " world"]) == "hello world"
