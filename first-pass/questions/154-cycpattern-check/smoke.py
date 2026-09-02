# solution.py — Bool-accumulator rewrite (no early return); see solution.py header.


def cycpattern_check(a, b):
    l = len(b)
    pat = b + b
    found = False
    i = 0
    j = 0
    for i in range(len(a) - l + 1):
        for j in range(l + 1):
            if a[i:i+l] == pat[j:j+l]:
                found = True
    return found


# Smoke checks — the HumanEval/154 dataset `check` cases (bare-bool asserts).
assert not cycpattern_check("xyzw", "xyw")
assert cycpattern_check("yello", "ell")
assert not cycpattern_check("whattup", "ptut")
assert cycpattern_check("efef", "fee")
assert not cycpattern_check("abab", "aabb")
assert cycpattern_check("winemtt", "tinem")
