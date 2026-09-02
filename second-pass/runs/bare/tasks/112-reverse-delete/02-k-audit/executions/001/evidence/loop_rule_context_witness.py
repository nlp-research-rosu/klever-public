#!/usr/bin/env python3
"""Real-Python behavior after the filtering loop observes loop target `ch`."""


def reverse_delete(s, c):
    result = ""
    for ch in s:
        if ch not in c:
            result = result + ch
    return ch


if __name__ == "__main__":
    print(reverse_delete("ab", ""))
