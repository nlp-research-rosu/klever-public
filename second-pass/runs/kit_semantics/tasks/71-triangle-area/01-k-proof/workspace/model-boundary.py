import math

from solution import triangle_area


result = triangle_area(float("nan"), 3.0, 4.0)
assert math.isnan(result)
print("CPython result: NaN")
