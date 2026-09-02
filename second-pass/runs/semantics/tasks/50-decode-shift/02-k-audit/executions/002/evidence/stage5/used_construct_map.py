#!/usr/bin/env python3
"""Map every constructor in solution.mpy to declarations and semantic occurrences."""

from __future__ import annotations

import re
from pathlib import Path


solution = Path("/tmp/audit-work/fresh/solution.regenerated.mpy").read_text(encoding="utf-8")
constructors = sorted(set(re.findall(r"\b([A-Z][A-Za-z0-9_]*)\s*\(", solution)))
k_files = [
    Path("/tmp/audit-work/fresh/reference-semantics/semantics.k"),
    *sorted(Path("/tmp/audit-work/fresh/reference-semantics/semantics").glob("*.k")),
    Path("/tmp/audit-work/fresh/verification.k"),
]

missing = []
for constructor in constructors:
    declaration_hits = []
    rule_hits = []
    pattern = re.compile(rf"\b{re.escape(constructor)}\s*\(")
    declaration_pattern = re.compile(rf'"{re.escape(constructor)}"\s+"\("')
    for path in k_files:
        lines = path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, 1):
            if not pattern.search(line):
                continue
            rel = path.relative_to(Path("/tmp/audit-work/fresh"))
            hit = f"{rel}:{line_number}:{line.strip()}"
            if "syntax " in line:
                declaration_hits.append(hit)
            if "rule " in line or "<k>" in line:
                rule_hits.append(hit)
        for index, line in enumerate(lines):
            if not re.match(r"^\s*syntax\b", line):
                continue
            stop = index + 1
            while stop < len(lines):
                candidate = lines[stop]
                if not candidate.strip():
                    break
                if re.match(
                    r"^\s*(syntax|rule|context|configuration|module|endmodule|imports)\b",
                    candidate,
                ):
                    break
                stop += 1
            block = "\n".join(lines[index:stop])
            if declaration_pattern.search(block):
                rel = path.relative_to(Path("/tmp/audit-work/fresh"))
                declaration_hits.append(
                    f"{rel}:{index + 1}:{' '.join(part.strip() for part in block.splitlines())}"
                )
    if not declaration_hits:
        missing.append(constructor)
    print(f"CONSTRUCTOR {constructor}")
    print("  declarations:")
    for hit in declaration_hits:
        print(f"    {hit}")
    print("  rule_occurrences:")
    for hit in rule_hits:
        print(f"    {hit}")

print(f"constructors={len(constructors)}")
print(f"missing_declarations={missing!r}")
raise SystemExit(bool(missing))
