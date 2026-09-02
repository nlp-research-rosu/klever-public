#!/usr/bin/env python3
"""Check that solutionProgram's RHS is the exact submitted MPY term."""

from pathlib import Path

mpy_path = Path("/tmp/audit-work/rebuild/submitted-solution.mpy")
wrapper_path = Path("/tmp/audit-work/rebuild/solution-program.k")

mpy_text = mpy_path.read_text(encoding="utf-8")
wrapper_text = wrapper_path.read_text(encoding="utf-8")
marker = "rule solutionProgram =>"
start = wrapper_text.index(marker) + len(marker)
end = wrapper_text.index("\nendmodule", start)
embedded_text = wrapper_text[start:end]

normalize = lambda value: "".join(value.split())
mpy_normalized = normalize(mpy_text)
embedded_normalized = normalize(embedded_text)

print("submitted_mpy=", mpy_path)
print("wrapper=", wrapper_path)
print("submitted_normalized_length=", len(mpy_normalized))
print("embedded_normalized_length=", len(embedded_normalized))
print("normalized_terms_identical=", mpy_normalized == embedded_normalized)
if mpy_normalized != embedded_normalized:
    raise SystemExit(1)
