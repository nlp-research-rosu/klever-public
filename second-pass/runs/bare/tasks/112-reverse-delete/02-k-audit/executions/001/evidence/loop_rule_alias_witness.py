#!/usr/bin/env python3
"""Real-Python behavior for the semantic loop rule's aliasing witness."""


def reverse_delete(s, c):
    result = ""
    for ch in s:
        if ch not in result:
            result = result + ch
    return (result, result == result[::-1])


if __name__ == "__main__":
    print(reverse_delete("aba", ""))
