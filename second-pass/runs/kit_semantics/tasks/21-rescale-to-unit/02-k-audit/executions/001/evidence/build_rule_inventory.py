#!/usr/bin/env python3
"""Enumerate every K declaration/rule/context/claim in the audited source tree."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/proof")
OUTPUT = Path("/audit-output/evidence/rule_inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule_inventory_summary.txt")

sources = sorted((ROOT / "reference-semantics").rglob("*.k"))
sources += [ROOT / "verification.k", ROOT / "spec.k"]

start_re = re.compile(
    r"^(module\b|imports\b|configuration\b|syntax\b|context\b|rule\b|claim\b|endmodule\b)"
)


def verification_basis(line: int) -> str:
    if 7 <= line <= 10:
        return "exhaustive recursive float-domain predicate"
    if 14 <= line <= 15:
        return "definedness predicate equals supplied isFloat sort predicate"
    if 17 <= line <= 30:
        return "guarded Val-to-Float projection and exact definedness characterization"
    if 34 <= line <= 37:
        return "dynamic-sort twin of supplied Float subtraction; overlap agrees"
    if 42 <= line <= 49:
        return "conservative aliases naming supplied minFloat/maxFloat primitives"
    if 52 <= line <= 82:
        return "exhaustive descending pure extrema-summary definitions"
    if 87 <= line <= 108:
        return "exhaustive descending pure scale accumulator matching append expression"
    if 113 <= line <= 116:
        return "exhaustive descending pure final-loop-target summary"
    return "module/import structure"


def emit_record(path: Path, line: int, statement: str) -> dict[str, str]:
    first = statement.lstrip().split(None, 1)[0]
    relative = path.relative_to(ROOT).as_posix()
    attributes = []
    for marker in [
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "priority",
        "simplification",
        "concrete",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
        "owise",
        "preserves-definedness",
    ]:
        if re.search(rf"\b{re.escape(marker)}\b", statement):
            attributes.append(marker)

    if first == "rule":
        if "simplification" in attributes:
            subtype = "simplification-rule"
        elif "priority" in attributes:
            subtype = "priority-rule"
        elif "concrete" in attributes:
            subtype = "concrete-rule"
        else:
            subtype = "ordinary-rule"
    elif first == "syntax":
        if "no-evaluators" in attributes or "symbol" in attributes:
            subtype = "opaque-symbol-declaration"
        elif "function" in attributes or "functional" in attributes or "total" in attributes:
            subtype = "function-declaration"
        else:
            subtype = "syntax-declaration"
    else:
        subtype = first

    if relative.startswith("reference-semantics/"):
        decision = "ACCEPTED_SUPPLIED_LEVEL"
        basis = (
            "byte-identical supplied baseline; selected SUPPLIED_SEMANTICS boundary; "
            "used rules separately traced"
        )
    elif relative == "verification.k":
        decision = "REVIEWED_SOUND"
        basis = verification_basis(line)
    elif relative == "spec.k" and first == "claim":
        decision = "RECONSTRUCTED_TOP"
        basis = "fresh four-claim proof closed; adequacy and non-vacuity reviewed separately"
    else:
        decision = "STRUCTURAL"
        basis = "module/import/spec structure"

    return {
        "source": relative,
        "line": str(line),
        "kind": first,
        "subtype": subtype,
        "attributes": ",".join(attributes) if attributes else "-",
        "decision": decision,
        "basis": basis,
        "statement": re.sub(r"\s+", " ", statement).strip(),
    }


records: list[dict[str, str]] = []
for path in sources:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[int] = []
    for index, line in enumerate(lines):
        # File-level `requires` has no indentation. Indented `requires` belongs
        # to the preceding rule/claim and must stay in that inventory record.
        if line.startswith("requires ") or start_re.match(line.strip()):
            starts.append(index)
    for offset, start in enumerate(starts):
        end = starts[offset + 1] if offset + 1 < len(starts) else len(lines)
        stripped = lines[start].strip()
        first = stripped.split(None, 1)[0]
        if first == "endmodule":
            statement = stripped
        else:
            body_lines = []
            for line in lines[start:end]:
                clean = line.split("//", 1)[0].strip()
                if clean:
                    body_lines.append(clean)
            statement = " ".join(body_lines)
        records.append(emit_record(path, start + 1, statement))

fields = [
    "source",
    "line",
    "kind",
    "subtype",
    "attributes",
    "decision",
    "basis",
    "statement",
]
with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=fields, dialect="excel-tab")
    writer.writeheader()
    writer.writerows(records)

kind_counts = Counter(record["kind"] for record in records)
subtype_counts = Counter(record["subtype"] for record in records)
source_counts = Counter(record["source"] for record in records)
summary_lines = [
    f"sources={len(sources)}",
    f"records={len(records)}",
    f"kind_counts={dict(sorted(kind_counts.items()))}",
    f"subtype_counts={dict(sorted(subtype_counts.items()))}",
    "per_source:",
]
summary_lines.extend(f"  {source}: {count}" for source, count in sorted(source_counts.items()))
SUMMARY.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
print("\n".join(summary_lines))
print(f"inventory={OUTPUT}")
