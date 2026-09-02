def max_element(l: list):
    return max(l)


# CPython and the trusted canonical function return "😀". The supplied
# concrete string-literal rule only accepts ASCII code points.
assert max_element(["é", "😀", "Ω"]) == "😀"
