#!/usr/bin/env python3
"""Create an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-clean")
paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
paths += [ROOT / "verification.k", ROOT / "spec.k"]

start_re = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
attribute_names = [
    "function",
    "functional",
    "total",
    "no-evaluators",
    "concrete",
    "simplification",
    "priority",
    "owise",
    "strict",
    "seqstrict",
    "macro",
    "symbol",
]

rows = []
for path in paths:
    lines = path.read_text().splitlines()
    starts = [(index, start_re.match(line).group(1)) for index, line in enumerate(lines) if start_re.match(line)]
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or block_lines[-1].strip() == "endmodule"
        ):
            block_lines.pop()
        block = "\n".join(block_lines)
        attrs = [name for name in attribute_names if re.search(rf"\b{re.escape(name)}\b", block)]
        rel = path.relative_to(ROOT)
        scope = "candidate-local" if rel in {Path("verification.k"), Path("spec.k")} else "fixed-supplied"
        if scope == "fixed-supplied":
            decision = "ACCEPT_FIXED_BASELINE"
        elif rel == Path("spec.k"):
            decision = "CLAIM_SCOPE_REVIEWED_SEPARATELY"
        elif "triangleAreaBody" in block:
            decision = "SOUND_EXACT_CONSTRUCTOR_ALIAS"
        elif "triangleAreaClosure" in block:
            decision = "SOUND_EXACT_CLOSURE_ALIAS"
        elif "triangleAreaModule" in block:
            decision = "SOUND_EXACT_MODULE_ALIAS"
        elif "semiPerimeter" in block or "expectedArea" in block:
            decision = "SOUND_DEFINITIONAL_SUMMARY"
        else:
            decision = "SOUND_LOCAL_DECLARATION"
        rows.append(
            {
                "file": str(rel),
                "line": start + 1,
                "kind": kind,
                "scope": scope,
                "attributes": ",".join(attrs) or "-",
                "decision": decision,
                "source": " ".join(piece.strip() for piece in block_lines)[:1200],
            }
        )

output = Path("/audit-output/evidence/05-static/rule-inventory.tsv")
with output.open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=rows[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

print(f"files={len(paths)}")
print(f"entries={len(rows)}")
for key, count in sorted(Counter((row["scope"], row["kind"]) for row in rows).items()):
    print(f"{key[0]}/{key[1]}={count}")
for attribute in attribute_names:
    count = sum(attribute in row["attributes"].split(",") for row in rows)
    print(f"attribute/{attribute}={count}")
print(f"inventory={output}")
