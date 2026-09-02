#!/usr/bin/env python3
"""Python behavior corresponding to for_bridge_context_witness.mpy."""


def reverse_delete(s, c):
    ch = "OLD"
    result = ""
    for ch in s:
        if ch not in c:
            result = result + ch
    return ch


if __name__ == "__main__":
    result = reverse_delete("a", "")
    print(f"python_result={result!r}")
    assert result == "a"
