from typing import List


def all_prefixes(string: str) -> List[str]:
    prefixes = []
    prefix = ""
    char = ""
    for char in string:
        prefix = prefix + char
        prefixes.append(prefix)
    return prefixes
