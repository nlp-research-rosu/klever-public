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
