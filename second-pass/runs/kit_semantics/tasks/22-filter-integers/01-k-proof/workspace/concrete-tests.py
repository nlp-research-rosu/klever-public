from typing import List, Any


def filter_integers(values: List[Any]) -> List[int]:
    """Filter a list to the values that are instances of ``int``."""
    result = []
    for value in values:
        if isinstance(value, int):
            result.append(value)
    return result


assert filter_integers(["a", 3.14, 5]) == [5]
assert filter_integers([1, 2, 3, "abc", {}, []]) == [1, 2, 3]
assert filter_integers([True, False, 0, None, 2.0]) == [True, False, 0]
assert filter_integers([]) == []
