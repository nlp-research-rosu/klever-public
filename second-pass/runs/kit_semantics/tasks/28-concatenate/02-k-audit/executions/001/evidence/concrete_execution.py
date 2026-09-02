from typing import List


def concatenate(strings: List[str]) -> str:
    result = ""
    string = ""
    for string in strings:
        result += string
    return result


empty = concatenate([])
single_empty = concatenate([""])
single = concatenate(["q"])
example = concatenate(["a", "b", "c"])
mixed = concatenate(["", "xy", "", "z"])
