def flip_case(string: str) -> str:
    return string.swapcase()


# The supplied K semantics models case conversion as ASCII-only, so U+00E9 is
# left unchanged there. CPython instead maps it to U+00C9.
assert flip_case(chr(233)) == chr(233)
