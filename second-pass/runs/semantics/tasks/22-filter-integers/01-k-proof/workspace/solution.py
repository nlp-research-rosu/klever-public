from typing import List, Any


def filter_integers(values: List[Any]) -> List[int]:
    """Filter values, retaining only integers in their original order."""
    result = []
    for value in values:
        if isinstance(value, int):
            result.append(value)
    return result
