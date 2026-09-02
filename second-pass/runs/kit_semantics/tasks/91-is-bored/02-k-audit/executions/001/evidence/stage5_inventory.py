#!/usr/bin/env python3
"""Emit a source-level inventory of every K declaration and rule in audit scope."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path("/tmp/audit-work/case91")

FILES = [ROOT / "reference-semantics" / "semantics.k"]
FILES += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
FILES += [
    ROOT / "verification-base.k",
    ROOT / "verification.k",
    ROOT / "connection.k",
    ROOT / "connection-spec.k",
    ROOT / "connection-mutation-spec.k",
    ROOT / "loop-spec.k",
    ROOT / "spec.k",
    ROOT / "spec-vacuity.k",
    ROOT / "mutation.k",
    ROOT / "mutation-spec.k",
]

START = re.compile(r"^\s*(syntax|configuration|context|rule|claim)\b")


def material(path: Path, line: int, kind: str) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in {
        "verification-base.k",
        "verification.k",
        "connection-spec.k",
        "loop-spec.k",
        "spec.k",
    }:
        return True
    if rel == "connection.k":
        return False
    if rel == "reference-semantics/semantics/syntax.k":
        return True
    ranges = {
        "reference-semantics/semantics/core.k": [
            (13, 60),
            (68, 70),
            (117, 127),
            (130, 181),
            (185, 205),
            (208, 210),
            (218, 220),
            (238, 244),
        ],
        "reference-semantics/semantics/iter.k": [(8, 8)],
        "reference-semantics/semantics/operators.k": [(14, 20)],
        "reference-semantics/semantics/int.k": [(9, 12)],
        "reference-semantics/semantics/bool.k": [(24, 36)],
        "reference-semantics/semantics/str.k": [(7, 26)],
        "reference-semantics/semantics/methods.k": [
            (9, 10),
            (46, 55),
            (85, 86),
        ],
        "reference-semantics/semantics/controls.k": [
            (8, 31),
            (50, 74),
            (84, 91),
        ],
        "reference-semantics/semantics/functions.k": [
            (8, 20),
            (62, 90),
        ],
        "reference-semantics/semantics/call.k": [
            (15, 32),
            (69, 75),
        ],
        "reference-semantics/semantics/tuple.k": [(30, 41)],
    }
    return any(lo <= line <= hi for lo, hi in ranges.get(rel, []))


def flags(block: str) -> list[str]:
    found = []
    for name, pattern in [
        ("function", r"\bfunction\b"),
        ("functional", r"\bfunctional\b"),
        ("total", r"\btotal\b"),
        ("symbol", r"\bsymbol\s*\("),
        ("opaque", r"\bno-evaluators\b"),
        ("priority", r"\bpriority\s*\("),
        ("simplification", r"\bsimplification\b"),
        ("macro-rec", r"\bmacro-rec\b"),
        ("macro", r"\bmacro\b"),
        ("concrete", r"\bconcrete\b"),
        ("owise", r"\bowise\b"),
        ("strict", r"\bstrict\b"),
        ("seqstrict", r"\bseqstrict\b"),
    ]:
        if re.search(pattern, block):
            found.append(name)
    return found


def normalized(block: list[str]) -> str:
    pieces = []
    for raw in block:
        stripped = raw.strip()
        if not stripped or stripped.startswith("//"):
            continue
        pieces.append(stripped)
    return " ".join(pieces).replace("|", "&#124;")


records = []
opaque_symbols = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, text in enumerate(lines):
        match = START.match(text)
        if match:
            starts.append((index, match.group(1)))
    for offset, (index, kind) in enumerate(starts):
        end = starts[offset + 1][0] if offset + 1 < len(starts) else len(lines)
        block_lines = lines[index:end]
        block = "\n".join(
            line for line in block_lines if not line.lstrip().startswith("//")
        )
        rel = path.relative_to(ROOT).as_posix()
        is_material = material(path, index + 1, kind)
        if rel.startswith("reference-semantics/"):
            decision = (
                "ACCEPTED_MATERIAL_FIXED_MODEL"
                if is_material
                else "INERT_FIXED_MODEL_NO_CLAIM_DEPENDENCY"
            )
        elif rel in {
            "connection-mutation-spec.k",
            "spec-vacuity.k",
            "mutation.k",
            "mutation-spec.k",
        }:
            decision = "UNTRUSTED_NEGATIVE_EVIDENCE_NOT_POSITIVE_DEPENDENCY"
        elif kind == "claim":
            decision = "FRESHLY_RECONSTRUCTED_TOP_REVIEWED"
        elif rel == "connection.k":
            decision = "IMPORT_ONLY"
        else:
            decision = "ACCEPTED_PROOF_LOCAL"
        records.append(
            {
                "file": rel,
                "line": index + 1,
                "kind": kind,
                "flags": ",".join(flags(block)) or "-",
                "material": "yes" if is_material else "no",
                "decision": decision,
                "source": normalized(block_lines),
            }
        )
        if "no-evaluators" in block:
            for symbol in re.findall(r"symbol\(([^)]+)\)", block):
                opaque_symbols.append(
                    (path.relative_to(ROOT).as_posix(), index + 1, symbol)
                )

print("# Exhaustive K source declaration and rule inventory")
print()
print(
    "Generated by `python3 /audit-output/evidence/stage5_inventory.py` "
    "from the clean scratch copy. Each row begins at a source declaration; "
    "multi-line bodies are normalized into the final column."
)
print()
print("| # | File:line | Kind | Attributes/class | Material | Review disposition | Source block |")
print("|---:|---|---|---|---|---|---|")
for number, record in enumerate(records, 1):
    print(
        f"| {number} | `{record['file']}:{record['line']}` | "
        f"{record['kind']} | {record['flags']} | {record['material']} | "
        f"{record['decision']} | `{record['source']}` |"
    )

print()
print("## Counts")
print()
print(f"TOTAL_RECORDS={len(records)}")
for (kind, decision), count in sorted(
    Counter((record["kind"], record["decision"]) for record in records).items()
):
    print(f"{kind} {decision}={count}")
for flag, count in sorted(
    Counter(
        flag
        for record in records
        for flag in ([] if record["flags"] == "-" else record["flags"].split(","))
    ).items()
):
    print(f"FLAG_{flag}={count}")
print(f"OPAQUE_SYMBOL_COUNT={len(opaque_symbols)}")
for rel, line, symbol in opaque_symbols:
    print(f"OPAQUE_SYMBOL {rel}:{line} {symbol}")
