def is_happy(s):
    happy = True
    i = 0
    p1 = 0
    p2 = 0
    code = 0
    c = ""
    for c in s:
        code = ord(c)
        if i >= 2:
            if code == p1 or p1 == p2 or code == p2:
                happy = False
        p2 = p1
        p1 = code
        i = i + 1
    return i >= 3 and happy


# HumanEval/80 test cases (the dataset `check`); returns a bool (bare-bool asserts).
assert not is_happy("a")
assert not is_happy("aa")
assert is_happy("abcd")
assert not is_happy("aabb")
assert is_happy("adb")
assert not is_happy("xyy")
assert is_happy("iopaxpoi")
assert not is_happy("iopaxioi")
