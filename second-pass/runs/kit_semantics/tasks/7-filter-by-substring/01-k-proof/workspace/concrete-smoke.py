from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    result = []
    string = ""
    for string in strings:
        if substring in string:
            result.append(string)
    return result


assert filter_by_substring([], "a") == []
assert filter_by_substring(["abc", "bacd", "cde", "array"], "a") == [
    "abc",
    "bacd",
    "array",
]
