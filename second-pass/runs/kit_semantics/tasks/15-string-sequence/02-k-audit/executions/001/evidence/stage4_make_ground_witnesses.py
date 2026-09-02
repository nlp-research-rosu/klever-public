#!/usr/bin/env python3
"""Specialize both candidate claims at the satisfying witness n=5."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def int_seq(text: str) -> str:
    term = ".IntSeq"
    for code in reversed(text.encode("ascii")):
        term = f"iCons({code}, {term})"
    return term


spec_path = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else "/tmp/audit-work/15-string-sequence/candidate-src/spec.k"
)
text = spec_path.read_text(encoding="utf-8")

loop_start = text.index("  claim [loop-invariant]:")
entry_start = text.index("  claim [string-sequence]:")
module_end = text.rindex("endmodule")
loop = text[loop_start:entry_start].rstrip()
entry = text[entry_start:module_end].rstrip()

initial = int_seq("0")
expected = int_seq("0 1 2 3 4 5")

loop = loop.replace("[loop-invariant]", "[loop-ground-n5]")
loop_result_pattern = re.compile(
    r'"result"\s*\|->\s*\(str\(ACC\)\s*=>\s*'
    r"str\(sequenceAcc\(ACC,\s*I,\s*N\)\)\)"
)
loop, replacements = loop_result_pattern.subn(
    f'"result" |-> (str({initial}) => str({expected}))', loop
)
if replacements != 1:
    raise RuntimeError(f"unexpected loop result replacement count: {replacements}")
loop = re.sub(r"\bI\b", "1", loop)
loop = re.sub(r"\bN\b", "5", loop)

entry = entry.replace("[string-sequence]", "[entry-ground-n5]")
entry = entry.replace("Call(Name(\"string_sequence\"), Int(N), .Exprs)", 'Call(Name("string_sequence"), Int(5), .Exprs)')
entry = entry.replace("str(stringSequenceCodes(N))", f"str({expected})")
if "Int(N)" in entry or "stringSequenceCodes(N)" in entry:
    raise RuntimeError("entry specialization was incomplete")

print('requires "verification.k"')
print()
print("module STAGE4-GROUND")
print("  imports VERIFICATION")
print()
print(loop)
print()
print(entry)
print("endmodule")
