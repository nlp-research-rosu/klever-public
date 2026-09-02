#!/usr/bin/env python3
"""Decode the observed result heaps in the fresh LLVM krun log."""

from __future__ import annotations

import re
from pathlib import Path


LOG = Path("/audit-output/evidence/concrete-run.log")


def heap_entry_line(text: str, address: int) -> str:
    pattern = re.compile(rf"^    {address} \|-> list \(.*$", re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        raise AssertionError(f"heap entry {address} not found")
    return match.group(0)


def balanced_segment(text: str, open_paren: int) -> str:
    depth = 0
    for index in range(open_paren, len(text)):
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
            if depth == 0:
                return text[open_paren : index + 1]
    raise AssertionError("unbalanced K term")


def decode_strings(line: str) -> list[str]:
    decoded = []
    cursor = 0
    while True:
        start = line.find("str (", cursor)
        if start < 0:
            return decoded
        open_paren = line.find("(", start)
        segment = balanced_segment(line, open_paren)
        codes = [int(code) for code in re.findall(r"iCons \( (-?\d+) ,", segment)]
        decoded.append("".join(chr(code) for code in codes))
        cursor = open_paren + len(segment)


def main() -> int:
    text = LOG.read_text(encoding="utf-8")
    assert "<k>\n    .K\n  </k>" in text
    assert "<exc>\n    NoExc\n  </exc>" in text
    assert "<exit-code>\n    0\n  </exit-code>" in text
    assert '"observed_example" |-> ref ( 1 )' in text
    assert '"observed_boundaries" |-> ref ( 3 )' in text
    assert '"observed_empty" |-> ref ( 5 )' in text

    expected_example = ["A+", "B", "C-", "C", "A-"]
    expected_boundaries = [
        "A+", "A", "A-", "A-", "B+", "B+", "B", "B", "B-",
        "B-", "C+", "C+", "C", "C", "C-", "C-", "D+", "D+",
        "D", "D", "D-", "D-", "E", "E", "A",
    ]
    actual_example = decode_strings(heap_entry_line(text, 1))
    actual_boundaries = decode_strings(heap_entry_line(text, 3))
    empty_line = heap_entry_line(text, 5)

    assert actual_example == expected_example, (actual_example, expected_example)
    assert actual_boundaries == expected_boundaries, (
        actual_boundaries,
        expected_boundaries,
    )
    assert "list ( .ValSeq )" in empty_line
    print(f"example={actual_example}")
    print(f"boundaries={actual_boundaries}")
    print("empty=[]")
    print("concrete_output_match=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
