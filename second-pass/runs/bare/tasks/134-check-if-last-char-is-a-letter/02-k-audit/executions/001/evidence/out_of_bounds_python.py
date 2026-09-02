#!/usr/bin/env python3
"""Ground oracle for the generated semantics' negative-index rule."""

text = "a"
try:
    result = text[-2]
    print(("return", result))
except Exception as error:
    print(("raise", type(error).__name__, str(error)))
