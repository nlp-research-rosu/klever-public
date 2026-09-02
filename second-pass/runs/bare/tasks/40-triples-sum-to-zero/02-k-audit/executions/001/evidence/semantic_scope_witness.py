#!/usr/bin/env python3
"""CPython sides of two generated-semantics scope/mismatch witnesses."""


def direct_index_one(l: list[int]):
    return l[1]


def fallthrough(l: list[int]):
    pass


values = [10, 20, 30]
print(f"direct_index_one({values!r})={direct_index_one(values)!r}")
print(f"fallthrough({values!r})={fallthrough(values)!r}")
assert direct_index_one(values) == 20
assert fallthrough(values) is None
