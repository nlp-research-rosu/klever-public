#!/usr/bin/env python3
"""Create a fresh false result obligation for the satisfying input n=5."""

from __future__ import annotations

import sys
from pathlib import Path


def int_seq(text: str) -> str:
    term = ".IntSeq"
    for code in reversed(text.encode("ascii")):
        term = f"iCons({code}, {term})"
    return term


path = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else "/tmp/audit-work/15-string-sequence/candidate-src/stage4-ground.k"
)
text = path.read_text(encoding="utf-8")
text = text.replace("module STAGE4-GROUND", "module STAGE6-FALSE")
text = text.replace("[entry-ground-n5]", "[false-entry-result-n5]")

true_result = int_seq("0 1 2 3 4 5")
false_result = int_seq("0 1 2 3 4 6")
replacements = text.count(true_result)
if replacements != 2:
    raise RuntimeError(f"unexpected true-result occurrence count: {replacements}")
text = text.replace(true_result, false_result)

# The executable program term is untouched: only literal destination values in
# the two claims changed. The selected entry claim still loads/calls n=5.
if 'Call(Name("string_sequence"), Int(5), .Exprs)' not in text:
    raise RuntimeError("satisfying input n=5 is not present")
print(text, end="")
