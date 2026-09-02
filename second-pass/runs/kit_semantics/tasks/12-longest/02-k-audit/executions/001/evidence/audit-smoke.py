from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    if not strings:
        return None

    result = strings[0]
    string = result
    for string in strings:
        if len(string) > len(result):
            result = string

    return result


assert longest([]) is None
assert longest([""]) == ""
assert longest(["a", "b", "c"]) == "a"
assert longest(["a", "bb", "ccc"]) == "ccc"
assert longest(["aa", "b", "cc"]) == "aa"
assert longest(["a", "bb", "c", "dddd"]) == "dddd"
