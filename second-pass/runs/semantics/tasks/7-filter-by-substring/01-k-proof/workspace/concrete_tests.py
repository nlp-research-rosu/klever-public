from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    result = []
    for string in strings:
        if substring in string:
            result.append(string)
    return result


assert filter_by_substring([], "a") == []
assert filter_by_substring(["abc", "bacd", "cde", "array"], "a") == ["abc", "bacd", "array"]
assert filter_by_substring(["", "aa", "b"], "") == ["", "aa", "b"]
assert filter_by_substring(["x", "xx", "y"], "xx") == ["xx"]
assert filter_by_substring(["abc", "def"], "z") == []
