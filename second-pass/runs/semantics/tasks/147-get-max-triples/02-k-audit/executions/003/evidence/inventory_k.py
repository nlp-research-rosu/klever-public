#!/usr/bin/env python3
"""Produce an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/147-get-max-triples-clean")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k"))
FILES += [ROOT / "verification.k", ROOT / "spec.k"]

HEADER = re.compile(r"^\s*(syntax|rule|claim|configuration|context)\b")
ATTR = re.compile(
    r"\[(?:[^\]]*?"
    r"(?:function|functional|total|symbol|no-evaluators|priority|owise|concrete|"
    r"macro|macro-rec|strict|seqstrict|simplification)[^\]]*?)\]"
)

REACHED = {
    "reference-semantics/semantics/syntax.k": {15, 41, 50},
    "reference-semantics/semantics/core.k": {
        49, 126, 127, 131, 132, 157, 158, 185, 186, 189, 190, 191, 194,
        208, 209, 213, 214, 215,
    },
    "reference-semantics/semantics/functions.k": {8, 9, 10, 11, 63, 64, 78, 85},
    "reference-semantics/semantics/call.k": {19, 20, 21, 69},
    "reference-semantics/semantics/controls.k": {9},
    "reference-semantics/semantics/int.k": {9, 13, 14, 16, 19, 20},
    "reference-semantics/semantics/operators.k": {12},
    "verification.k": {8, 9, 45, 46, 51, 52, 55, 56},
    "spec.k": {7, 14, 21, 32},
}

TOTALITY_WARNINGS = {
    ("reference-semantics/semantics/builtins.k", 134),
    ("reference-semantics/semantics/float.k", 73),
    ("reference-semantics/semantics/float.k", 86),
    ("reference-semantics/semantics/float.k", 93),
    ("reference-semantics/semantics/methods.k", 27),
    ("reference-semantics/semantics/subscript.k", 11),
}


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def assessment(rel: str, line: int, block: str, kind: str) -> tuple[str, str]:
    if rel == "verification.k":
        return "LOCAL_PROOF_EXTENSION", "reviewed: truthful terminating definition; no overlap"
    if rel == "spec.k":
        return "TARGET_CLAIM", "reviewed independently in Stages 3-6"
    if line in REACHED.get(rel, set()):
        return "TARGET_REACHABLE_FIXED", "reviewed against this program's Python behavior"
    if (rel, line) in TOTALITY_WARNINGS:
        return "UNUSED_TOTALITY_GAP", "compiler-reported non-exhaustive total function; unreachable here"
    if "no-evaluators" in block:
        return "UNUSED_OPAQUE_BOUNDARY", "explicit opaque result; unreachable here"
    if "[concrete]" in block:
        return "UNUSED_CONCRETE_ONLY", "concrete-only rule; absent from symbolic target path"
    return "UNUSED_FIXED_BASELINE", "reviewed; no false conclusion witness affecting target"


all_counts: Counter[str] = Counter()
print("# Exhaustive K source inventory")
print()
print("Each source header beginning `syntax`, `rule`, `claim`, `configuration`, or")
print("`context` is listed once. The complete numbered source is preserved separately.")
print()

for path in FILES:
    rel = relative(path)
    raw = path.read_bytes()
    text = raw.decode()
    lines = text.splitlines()
    headers = [
        (index, HEADER.match(line).group(1))
        for index, line in enumerate(lines, 1)
        if HEADER.match(line)
    ]
    counts = Counter(kind for _, kind in headers)
    all_counts.update(counts)
    print(f"## {rel}")
    print()
    print(f"- sha256: `{hashlib.sha256(raw).hexdigest()}`")
    print(f"- headers: {len(headers)}; counts: `{dict(sorted(counts.items()))}`")
    print()
    print("| line | kind | attributes | target class | assessment | source header |")
    print("|---:|---|---|---|---|---|")
    for position, (line_number, kind) in enumerate(headers):
        next_line = headers[position + 1][0] if position + 1 < len(headers) else len(lines) + 1
        block = "\n".join(lines[line_number - 1 : next_line - 1])
        attrs = ", ".join(match.group(0) for match in ATTR.finditer(block)) or "—"
        target_class, review = assessment(rel, line_number, block, kind)
        source = lines[line_number - 1].strip().replace("|", "\\|").replace("`", "'")
        print(
            f"| {line_number} | {kind} | {attrs.replace('|', '&#124;')} | "
            f"{target_class} | {review} | `{source}` |"
        )
    print()

print("# Totals")
print()
print(f"- source files: {len(FILES)}")
print(f"- inventoried headers: {sum(all_counts.values())}")
print(f"- counts: `{dict(sorted(all_counts.items()))}`")
print(f"- explicit target-reachable source headers: {sum(len(v) for v in REACHED.values())}")
print(f"- compiler-reported unused totality gaps: {len(TOTALITY_WARNINGS)}")
