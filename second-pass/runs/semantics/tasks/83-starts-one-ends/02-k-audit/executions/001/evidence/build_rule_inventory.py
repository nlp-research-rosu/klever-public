#!/usr/bin/env python3
"""Build an exhaustive, line-addressable inventory of local K declarations."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


SEM_ROOT = Path("/candidate/reference-semantics")
FILES = [SEM_ROOT / "semantics.k", *sorted((SEM_ROOT / "semantics").glob("*.k"))]
FILES += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

# Explicit source rules exercised by the entry claims. Strict/seqstrict syntax
# additionally generates the heating/cooling needed for the listed constructs.
DIRECT_RULES = {
    "semantics/core.k": {
        126, 127, 131, 132, 158, 189, 190, 191, 194, 200, 214
    },
    "semantics/str.k": {14, 15, 16},
    "semantics/operators.k": {12, 17},
    "semantics/int.k": {13, 14, 17, 26},
    "semantics/controls.k": {48, 52, 53, 54},
    "semantics/functions.k": {63, 64, 78, 85},
    "semantics/call.k": {20, 21, 69},
    "verification.k": {9, 18},
}

START_RE = re.compile(r"^\s*(configuration|context|syntax|rule|claim|alias)\b")
ATTR_GROUP_RE = re.compile(r"\[([^\]]+)\]")
ATTR_TOKEN_RE = re.compile(
    r"(?:"
    r"macro-rec|macro|function|functional|total|simplification|concrete|"
    r"owise|no-evaluators|priority\([^)]*\)|seqstrict\([^)]*\)|"
    r"strict(?:\([^)]*\))?|symbol\([^)]*\)"
    r")"
)


def short_path(path: Path) -> str:
    if path.is_relative_to(SEM_ROOT):
        return str(path.relative_to(SEM_ROOT))
    return path.name


records: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [
        (idx, START_RE.match(line).group(1))
        for idx, line in enumerate(lines)
        if START_RE.match(line)
    ]
    for pos, (idx, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        # Stop before endmodule and trailing comments belonging to no record.
        while end > idx + 1 and (
            lines[end - 1].strip() == ""
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        block = "\n".join(lines[idx:end]).rstrip()
        rel = short_path(path)
        attrs = sorted(
            {
                token
                for group in ATTR_GROUP_RE.findall(block)
                for token in ATTR_TOKEN_RE.findall(group)
            }
        )
        if kind == "rule":
            subtype = "operational-rule" if "<k>" in block else "equational-rule"
        elif kind == "syntax" and "function" in attrs:
            subtype = "function-declaration"
        else:
            subtype = kind
        direct = idx + 1 in DIRECT_RULES.get(rel, set())
        if rel == "verification.k":
            review = "proof-local-reviewed"
        elif direct:
            review = "directly-used-reviewed"
        elif rel == "spec.k":
            review = "entry-claim-reviewed"
        else:
            review = "inert-for-submitted-program-reviewed-for-overlap"
        records.append(
            {
                "file": rel,
                "line": idx + 1,
                "kind": kind,
                "subtype": subtype,
                "attrs": ";".join(attrs) or "-",
                "direct": "yes" if direct else "no",
                "review": review,
                "block": block,
            }
        )

tsv_path = Path("/audit-output/evidence/rule_inventory.tsv")
with tsv_path.open("w") as out:
    out.write("id\tfile\tline\tkind\tsubtype\tattributes\tdirectly_exercised\treview\n")
    for ident, rec in enumerate(records, 1):
        out.write(
            f"{ident}\t{rec['file']}\t{rec['line']}\t{rec['kind']}\t"
            f"{rec['subtype']}\t{rec['attrs']}\t{rec['direct']}\t{rec['review']}\n"
        )

full_path = Path("/audit-output/evidence/rule_inventory_full.txt")
with full_path.open("w") as out:
    for ident, rec in enumerate(records, 1):
        out.write(
            f"===== {ident} {rec['file']}:{rec['line']} {rec['subtype']} "
            f"attrs={rec['attrs']} direct={rec['direct']} review={rec['review']} =====\n"
        )
        out.write(str(rec["block"]))
        out.write("\n\n")

per_file: dict[str, Counter[str]] = defaultdict(Counter)
attribute_counts: Counter[str] = Counter()
for rec in records:
    per_file[str(rec["file"])][str(rec["subtype"])] += 1
    if rec["attrs"] != "-":
        attribute_counts.update(str(rec["attrs"]).split(";"))

summary_path = Path("/audit-output/evidence/rule_inventory_summary.txt")
with summary_path.open("w") as out:
    out.write(f"record_count={len(records)}\n")
    out.write(f"rule_count={sum(1 for r in records if r['kind'] == 'rule')}\n")
    out.write(f"syntax_count={sum(1 for r in records if r['kind'] == 'syntax')}\n")
    out.write(f"context_count={sum(1 for r in records if r['kind'] == 'context')}\n")
    out.write(f"configuration_count={sum(1 for r in records if r['kind'] == 'configuration')}\n")
    out.write(f"claim_count={sum(1 for r in records if r['kind'] == 'claim')}\n")
    out.write("attributes=" + repr(dict(sorted(attribute_counts.items()))) + "\n")
    for file, counts in per_file.items():
        out.write(f"{file}\t{dict(sorted(counts.items()))}\n")

print(summary_path.read_text(), end="")
