from typing import List


def concatenate(strings: List[str]) -> str:
    result = ""
    for string in strings:
        result = result + string
    return result
