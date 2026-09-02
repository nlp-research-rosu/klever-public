from typing import List


def filter_by_prefix(strings: List[str], prefix: str) -> List[str]:
    result = []
    string = ""
    for string in strings:
        if string.startswith(prefix):
            result.append(string)
    return result


assert filter_by_prefix([], "a") == []
assert filter_by_prefix(["abc", "bcd", "cde", "array"], "a") == ["abc", "array"]
assert filter_by_prefix(["", "a", "ab"], "") == ["", "a", "ab"]
assert filter_by_prefix(["a", "aa", "ba"], "aa") == ["aa"]
