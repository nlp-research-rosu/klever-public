from typing import List, Any


def filter_integers(values: List[Any]) -> List[int]:
    """Filter a list to the values that are instances of ``int``."""
    result = []
    for value in values:
        if isinstance(value, int):
            result.append(value)
    return result
