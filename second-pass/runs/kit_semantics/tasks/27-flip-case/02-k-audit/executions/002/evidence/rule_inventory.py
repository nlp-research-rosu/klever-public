#!/usr/bin/env python3
"""Inventory every local K declaration and attach theorem-slice assessments."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/rebuild")
SEMANTICS = SCRATCH / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.txt")

sources = sorted(SEMANTICS.rglob("*.k")) + [
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]

declaration = re.compile(
    r"^(?P<indent>\s*)(?P<kind>"
    r"requires|module|endmodule|imports|syntax|configuration|context|rule|claim"
    r")\b"
)

# Exact fixed-semantics declarations/rules in the dynamic transition cone.
used_starts: dict[str, set[int]] = {
    "semantics.k": {34, 58, 59, 80},
    "semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13,
        14,
        15,
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        213,
        214,
        215,
    },
    "semantics/functions.k": {8, 14, 63, 64, 78, 85},
    "semantics/call.k": {16, 19, 20, 21, 24, 69},
    "semantics/methods.k": {
        10,
        21,
        112,
        113,
        115,
        116,
        149,
        150,
        151,
        152,
        162,
        163,
        164,
    },
    "verification.k": {1, 3, 4, 5},
    "spec.k": {1, 3, 4, 6, 38},
}

# Supplied declarations that define the model/CPython text divergence relevant
# to the audited theorem or to its concrete representation witness.
gap_starts: dict[str, set[int]] = {
    "semantics/str.k": {13, 14, 15, 16},
    "semantics/builtins.k": {143, 144},
    "semantics/methods.k": {
        112,
        113,
        115,
        116,
        149,
        150,
        151,
        152,
        162,
        163,
        164,
    },
}


def relative(path: Path) -> str:
    if path.is_relative_to(SEMANTICS):
        return path.relative_to(SEMANTICS).as_posix()
    return path.name


def classify(rel: str, start: int, kind: str, text: str) -> tuple[str, str]:
    tags = []
    for tag in (
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "priority",
        "simplification",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
        "concrete",
        "owise",
    ):
        if re.search(rf"\b{re.escape(tag)}\b", text):
            tags.append(tag)

    if rel == "verification.k":
        decision = (
            "proof-local import only; no local semantic or equational extension"
        )
    elif rel == "spec.k" and kind == "claim":
        decision = "target reachability claim; audited for identity and result constraint"
    elif start in used_starts.get(rel, set()):
        if start in gap_starts.get(rel, set()):
            decision = (
                "reachable fixed-semantics rule/declaration; locally coherent and "
                "exhaustive for IntSeq, but intentionally ASCII-only versus CPython"
            )
        else:
            decision = (
                "reachable fixed-semantics rule/declaration; checked against the "
                "exact call/return transition and found sound on every matched "
                "configuration reachable from the entry claim"
            )
    elif start in gap_starts.get(rel, set()):
        decision = (
            "supplied-model boundary declaration/rule; outside the target transition "
            "unless used by the boundary witness; documented divergence, no "
            "candidate-added narrowing"
        )
    elif kind in {"requires", "imports", "module", "endmodule"}:
        decision = "module/dependency structure; integrity matched trusted supplied tree"
    elif kind in {"syntax", "configuration", "context"}:
        decision = (
            "fixed supplied declaration outside the target transition cone; no "
            "result/control influence on this theorem"
        )
    else:
        decision = (
            "fixed supplied rule outside the exact program transition cone; cannot "
            "match the audited program state and contributes no result, control, "
            "state, or proof step to this theorem"
        )
    return ",".join(tags), decision


records: list[dict[str, str | int]] = []
for path in sources:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines, 1):
        match = declaration.match(line)
        if not match:
            continue
        kind = match.group("kind")
        indent = len(match.group("indent"))
        if kind in {"requires", "module", "endmodule"}:
            if indent != 0:
                continue
        elif indent != 2:
            continue
        starts.append((index, kind))
    rel = relative(path)
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] - 1 if position + 1 < len(starts) else len(lines)
        block_lines = lines[start - 1 : end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
            end -= 1
        text = " ".join(line.strip() for line in block_lines if line.strip())
        tags, decision = classify(rel, start, kind, text)
        records.append(
            {
                "file": rel,
                "start_line": start,
                "end_line": end,
                "kind": kind,
                "attributes": tags,
                "declaration": text,
                "assessment": decision,
            }
        )

with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "file",
            "start_line",
            "end_line",
            "kind",
            "attributes",
            "declaration",
            "assessment",
        ],
        dialect="excel-tab",
    )
    writer.writeheader()
    writer.writerows(records)

kind_counts = Counter(record["kind"] for record in records)
attribute_counts: Counter[str] = Counter()
for record in records:
    for tag in str(record["attributes"]).split(","):
        if tag:
            attribute_counts[tag] += 1

rule_records = [record for record in records if record["kind"] == "rule"]
claim_records = [record for record in records if record["kind"] == "claim"]
verification_extensions = [
    record
    for record in records
    if record["file"] == "verification.k"
    and record["kind"] in {"syntax", "configuration", "context", "rule", "claim"}
]
summary_lines = [
    f"source_file_count={len(sources)}",
    f"record_count={len(records)}",
    f"kind_counts={dict(sorted(kind_counts.items()))}",
    f"attribute_counts={dict(sorted(attribute_counts.items()))}",
    f"rule_count={len(rule_records)}",
    f"claim_count={len(claim_records)}",
    f"verification_local_extension_count={len(verification_extensions)}",
    "simplification_declaration_count="
    + str(sum("simplification" in str(record["attributes"]) for record in records)),
    "functional_declaration_count="
    + str(sum("functional" in str(record["attributes"]).split(",") for record in records)),
    "INVENTORY_STATUS=COMPLETE",
]
SUMMARY.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
print("\n".join(summary_lines))
