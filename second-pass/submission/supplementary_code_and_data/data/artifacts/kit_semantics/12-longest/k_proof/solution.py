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
