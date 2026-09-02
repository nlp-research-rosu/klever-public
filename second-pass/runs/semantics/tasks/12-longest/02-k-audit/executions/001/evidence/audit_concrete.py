from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    result = None
    string = None
    for string in strings:
        if result is None:
            result = string
        elif len(string) <= len(result):
            result = result
        elif len(string) > len(result):
            result = string
    return result

assert longest([]) is None
assert longest(["a", "b", "c"]) == "a"
assert longest(["a", "bb", "ccc"]) == "ccc"
assert longest(["bb", "a"]) == "bb"
assert longest(["aa", "bb"]) == "aa"
assert longest(["", "", ""]) == ""

