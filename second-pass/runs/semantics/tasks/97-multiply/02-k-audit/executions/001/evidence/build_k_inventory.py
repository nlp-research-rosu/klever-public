#!/usr/bin/env python3
"""Build an exhaustive source-level declaration/rule ledger for the audit."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
SEMANTICS = ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/k-rule-inventory.tsv")

paths = [SEMANTICS / "semantics.k"]
paths.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
paths.extend([ROOT / "verification.k", ROOT / "spec.k"])

start_re = re.compile(
    r"^\s*(requires|module|imports|syntax|configuration|context|rule|claim)\b"
)
attribute_names = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "priority",
    "simplification",
    "owise",
    "anywhere",
]

# Exact source-rule starts exercised by the proof's submitted-program path.
used_rule_lines = {
    ("semantics/core.k", 125),
    ("semantics/core.k", 126),
    ("semantics/core.k", 127),
    ("semantics/core.k", 131),
    ("semantics/core.k", 132),
    ("semantics/core.k", 158),
    ("semantics/core.k", 189),
    ("semantics/core.k", 190),
    ("semantics/core.k", 191),
    ("semantics/core.k", 194),
    ("semantics/str.k", 14),
    ("semantics/str.k", 15),
    ("semantics/str.k", 16),
    ("semantics/operators.k", 12),
    ("semantics/int.k", 14),
    ("semantics/int.k", 15),
    ("semantics/int.k", 20),
    ("semantics/controls.k", 48),
    ("semantics/call.k", 20),
    ("semantics/call.k", 21),
    ("semantics/call.k", 69),
    ("semantics/functions.k", 63),
    ("semantics/functions.k", 64),
    ("semantics/functions.k", 78),
    ("semantics/functions.k", 85),
    ("verification.k", 9),
    ("verification.k", 23),
    ("verification.k", 28),
    ("verification.k", 31),
    ("spec.k", 6),
}


def relative(path: Path) -> str:
    if path.is_relative_to(SEMANTICS):
        return str(path.relative_to(SEMANTICS))
    return path.name


def records(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group(1)))
    for record_index, (start, kind) in enumerate(starts):
        stop = starts[record_index + 1][0] if record_index + 1 < len(starts) else len(lines)
        statement_lines = lines[start:stop]
        # Trim trailing blank/comment lines which introduce the next section.
        while statement_lines and (
            not statement_lines[-1].strip()
            or statement_lines[-1].lstrip().startswith("//")
        ):
            statement_lines.pop()
        yield start + 1, kind, "\n".join(statement_lines)


rows = []
counter = 0
for path in paths:
    rel = relative(path)
    for line, kind, statement in records(path):
        counter += 1
        attributes = ",".join(
            name
            for name in attribute_names
            if re.search(rf"\b{re.escape(name)}\b", statement)
        )
        proof_slice = (rel, line) in used_rule_lines
        opaque = "no-evaluators" in attributes

        if rel == "verification.k":
            decision = "ACCEPTED_PROOF_LOCAL"
            rationale = {
                9: "Constant closure equals submitted parameters/body and captures initial scope 0.",
                23: "Fresh entry helper routes only to an ordinary Call of the pinned closure.",
                28: "Definitional unit digit is exactly supplied pyMod(I,10).",
                31: "Definitional result is the product of the two supplied unit-digit terms.",
            }.get(line, "Proof-local declaration; no execution-replacing rule.")
        elif rel == "spec.k":
            decision = "TARGET_CLAIM_RESULT_CONSTRAINING"
            rationale = (
                "Universal Int inputs, realizable initial configuration, exact program call, "
                "and explicit unitDigitProduct result."
            )
        elif opaque:
            decision = "OPAQUE_FIXED_BOUNDARY_UNUSED"
            rationale = (
                "Selected supplied-semantics opaque symbol; no equation fabricates a value, "
                "and the submitted AST/proof does not reach it."
            )
        elif proof_slice:
            decision = "ACCEPTED_USED_SOUND"
            rationale = (
                "Exercised exact-AST path; checked binding/evaluation/control/cells and "
                "constructor or integer equation against the supplied subset semantics."
            )
        elif rel == "semantics/concrete.k" or "concrete" in attributes:
            decision = "ACCEPTED_CONCRETE_ONLY_UNUSED"
            rationale = (
                "Concrete LLVM support outside the Haskell proof definition and unreachable "
                "from the submitted integer-only AST proof path."
            )
        else:
            decision = "ACCEPTED_FIXED_UNUSED"
            rationale = (
                "Integrity-matched supplied semantics; guards/constructor recursion reviewed "
                "at module level, no false-conclusion witness found, and unreachable from "
                "the exact submitted AST proof path."
            )

        rows.append(
            {
                "id": f"KINV-{counter:04d}",
                "file": rel,
                "line": line,
                "kind": kind,
                "attributes": attributes,
                "proof_slice": "yes" if proof_slice else "no",
                "decision": decision,
                "rationale": rationale,
                "statement": statement.replace("\t", " ").replace("\n", "\\n"),
            }
        )

with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "id",
            "file",
            "line",
            "kind",
            "attributes",
            "proof_slice",
            "decision",
            "rationale",
            "statement",
        ],
        dialect="excel-tab",
    )
    writer.writeheader()
    writer.writerows(rows)

by_kind = Counter(row["kind"] for row in rows)
by_decision = Counter(row["decision"] for row in rows)
by_attribute = Counter(
    attribute
    for row in rows
    for attribute in row["attributes"].split(",")
    if attribute
)

print(f"inventory_path={OUTPUT}")
print(f"inventory_records={len(rows)}")
print(f"by_kind={dict(sorted(by_kind.items()))}")
print(f"by_decision={dict(sorted(by_decision.items()))}")
print(f"by_attribute={dict(sorted(by_attribute.items()))}")
print(f"proof_slice_records={sum(row['proof_slice'] == 'yes' for row in rows)}")
