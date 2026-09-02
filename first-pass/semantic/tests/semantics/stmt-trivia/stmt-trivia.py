"""Module docstring: a bare-expression statement."""
from typing import List, Optional
import math


def f(xs: List[int]) -> int:
    """Function docstring."""
    3 + 4
    return len(xs)


assert f([1, 2, 3]) == 3
