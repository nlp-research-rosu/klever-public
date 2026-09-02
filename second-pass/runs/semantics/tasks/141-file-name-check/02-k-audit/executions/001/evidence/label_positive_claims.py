#!/usr/bin/env python3
"""Add selection labels to the six otherwise unchanged candidate claims."""

from pathlib import Path


source_path = Path("/tmp/audit-work/141-file-name-check/spec.k")
output_path = Path("/tmp/audit-work/141-file-name-check/spec-labeled.k")
labels = [
    "audit-reject-dot-count",
    "audit-reject-short",
    "audit-reject-first",
    "audit-reject-suffix",
    "audit-reject-digits",
    "audit-accept",
]

text = source_path.read_text(encoding="utf-8")
text = text.replace("module SPEC\n", "module SPEC-LABELED\n", 1)
text = text.replace("endmodule\n", "endmodule\n", 1)

needle = "  claim\n"
assert text.count(needle) == len(labels), text.count(needle)
for label in labels:
    text = text.replace(needle, f"  claim [{label}]:\n", 1)

output_path.write_text(text, encoding="utf-8")
print(output_path)
print("\n".join(labels))
