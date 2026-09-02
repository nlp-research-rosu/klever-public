#!/usr/bin/env python3
"""Enumerate and classify every local K declaration used by the audit."""

from __future__ import annotations

import collections
import csv
import hashlib
import json
import pathlib
import re


WORK = pathlib.Path("/tmp/audit-work/reconstruction")
OUTPUT = pathlib.Path("/audit-output/evidence/stage5_rule_inventory.tsv")
SUMMARY = pathlib.Path("/audit-output/evidence/stage5_rule_inventory_summary.json")
START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")

# Exact source declarations on the real execution path.  A declaration can
# contain multiple alternatives (for example Expr and Stmt); the REVIEW maps
# the used alternatives within those declarations.
MATERIAL: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {
        9,
        32,
        37,
        41,
        56,
        57,
        60,
        61,
    },
    "reference-semantics/semantics/core.k": {
        14,
        18,
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
        152,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        199,
        200,
        202,
        208,
        209,
        210,
        213,
        214,
        215,
        223,
        224,
        225,
    },
    "reference-semantics/semantics/iter.k": {8},
    "reference-semantics/semantics/list.k": {9, 10},
    "reference-semantics/semantics/tuple.k": {31, 32},
    "reference-semantics/semantics/controls.k": {
        9,
        20,
        51,
        52,
        53,
        54,
        65,
        69,
        71,
        72,
        73,
    },
    "reference-semantics/semantics/functions.k": {
        8,
        14,
        63,
        64,
        78,
        80,
        85,
    },
    "reference-semantics/semantics/call.k": {19, 20, 21, 69},
    "reference-semantics/semantics/operators.k": {12, 15, 16, 17},
    "reference-semantics/semantics/int.k": {9, 15, 19, 20, 26, 27},
}


def source_files() -> list[pathlib.Path]:
    files = sorted((WORK / "reference-semantics").rglob("*.k"))
    files.extend(
        [
            WORK / "verification-base.k",
            WORK / "verification.k",
            WORK / "spec.k",
            WORK / "connection-spec.k",
        ]
    )
    return files


def classify(rel: str, line: int, kind: str) -> tuple[str, str]:
    if rel == "verification-base.k":
        return (
            "PROOF_EXTENSION",
            "ACCEPT: audited for guards, coverage, overlap, descent, and value influence",
        )
    if rel == "verification.k":
        return (
            "OPERATIONAL_BRIDGE",
            "ACCEPT: exact match domain and state update are covered by CONNECTION-SPEC.loop",
        )
    if rel in {"spec.k", "connection-spec.k"}:
        return (
            "REACHABILITY_CLAIM",
            "ACCEPT: independently rebuilt/proved; adequacy reviewed separately",
        )
    if rel == "reference-semantics/semantics/concrete.k":
        return (
            "RUNTIME_ONLY_UNUSED",
            "NO_PROOF_PATH: imported only by MPY-KRUN, not by either proof definition",
        )
    if line in MATERIAL.get(rel, set()):
        return (
            "FIXED_MATERIAL",
            "ACCEPT: fixed-semantics declaration/rule on the submitted constructor path",
        )
    return (
        "FIXED_UNUSED",
        "NO_TARGET_PATH: head/construct is absent from submitted execution and proof summaries",
    )


rows: list[dict[str, str | int]] = []
for path in source_files():
    rel = path.relative_to(WORK).as_posix()
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for number, (start, kind) in enumerate(starts):
        end = starts[number + 1][0] if number + 1 < len(starts) else len(lines)
        statement_lines = lines[start:end]
        while statement_lines and (
            not statement_lines[-1].strip()
            or statement_lines[-1].lstrip().startswith("//")
            or statement_lines[-1].strip() == "endmodule"
        ):
            statement_lines.pop()
        statement = "\n".join(statement_lines)
        normalized = " ".join(
            part.strip()
            for part in statement_lines
            if part.strip() and not part.lstrip().startswith("//")
        )
        attributes = sorted(
            {
                token
                for token in [
                    "function",
                    "functional",
                    "total",
                    "no-evaluators",
                    "priority",
                    "simplification",
                    "concrete",
                    "symbolic",
                    "owise",
                    "macro",
                    "strict",
                    "seqstrict",
                    "preserves-definedness",
                ]
                if re.search(rf"\b{re.escape(token)}\b", statement)
            }
        )
        classification, decision = classify(rel, start + 1, kind)
        rows.append(
            {
                "id": len(rows) + 1,
                "file": rel,
                "line": start + 1,
                "kind": kind,
                "classification": classification,
                "attributes": ",".join(attributes) or "-",
                "statement_sha256": hashlib.sha256(statement.encode()).hexdigest(),
                "signature": normalized[:500],
                "decision": decision,
            }
        )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "id",
            "file",
            "line",
            "kind",
            "classification",
            "attributes",
            "statement_sha256",
            "signature",
            "decision",
        ],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)

summary = {
    "total": len(rows),
    "by_kind": dict(collections.Counter(str(row["kind"]) for row in rows)),
    "by_classification": dict(
        collections.Counter(str(row["classification"]) for row in rows)
    ),
    "by_file": dict(collections.Counter(str(row["file"]) for row in rows)),
    "inventory_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
}
SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
print(json.dumps(summary, indent=2, sort_keys=True))
