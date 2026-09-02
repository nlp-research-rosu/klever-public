from typing import List


def all_prefixes(string: str) -> List[str]:
    """Return all nonempty prefixes of string, shortest first."""
    prefixes = []
    for end in range(1, len(string) + 1):
        prefixes.append(string[:end])
    return prefixes
