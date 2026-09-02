from typing import List


def all_prefixes(string: str) -> List[str]:
    result = []
    i = 1
    while i <= len(string):
        result.append(string[:i])
        i = i + 1
    return result
