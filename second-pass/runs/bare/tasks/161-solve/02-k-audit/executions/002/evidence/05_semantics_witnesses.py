#!/usr/bin/env python3
"""Independent Python outcomes for the reviewer semantic-rule witnesses."""


def filter_false(s):
    return s.swapcase() if any(c.isalpha() for c in s if False) else s[::-1]


def swapcase_arg(s):
    return s.swapcase(1)


print("filter_false input='a' python_result=", repr(filter_false("a")))
try:
    swapcase_arg("a")
except Exception as err:
    print("swapcase_arg input='a' python_exception=", type(err).__name__, str(err))
else:
    raise AssertionError("Python unexpectedly accepted str.swapcase(1)")

print("unicode input='éa' python_result=", repr("éa".swapcase()))
print("unicode input='éa' python_codepoints=", [ord(c) for c in "éa".swapcase()])
print("unicode input='ß1' python_result=", repr("ß1".swapcase()))
print("unicode input='ß1' python_codepoints=", [ord(c) for c in "ß1".swapcase()])
