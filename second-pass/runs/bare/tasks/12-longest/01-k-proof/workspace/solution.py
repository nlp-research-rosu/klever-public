from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    if len(strings) == 0:
        return None

    result = strings[0]
    for string in strings:
        if len(string) > len(result):
            result = string

    return result
