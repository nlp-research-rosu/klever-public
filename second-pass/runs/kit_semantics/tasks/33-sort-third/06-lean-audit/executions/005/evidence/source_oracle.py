#!/usr/bin/env python3
values = ["b", 0, 0, "a"]
thirds = sorted(values[::3])
result = [
    thirds[index // 3] if index % 3 == 0 else value
    for index, value in enumerate(values)
]
print(f"input={values!r}")
print(f"third_position_slice={values[::3]!r}")
print(f"sorted_slice={thirds!r}")
print(f"source_result={result!r}")
