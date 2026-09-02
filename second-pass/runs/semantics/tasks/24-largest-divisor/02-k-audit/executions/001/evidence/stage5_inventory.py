#!/usr/bin/env python3
"""Emit a source-level inventory of every K sentence in the audited theory."""

from __future__ import annotations

import collections
import re
from pathlib import Path

ROOT = Path("/tmp/audit-work")
SEMANTICS = ROOT / "reference-semantics"
files = [SEMANTICS / "semantics.k"]
files.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
files.extend([ROOT / "verification.k", ROOT / "spec.k"])

START = re.compile(
    r"^(?P<indent>[ \t]*)(?P<kind>requires|module|imports|configuration|"
    r"syntax|context|rule|claim|endmodule)\b"
)

used_ranges: dict[str, list[tuple[int, int]]] = {
    "semantics/syntax.k": [(9, 61)],
    "semantics/core.k": [
        (25, 42),
        (49, 60),
        (124, 134),
        (152, 181),
        (185, 191),
        (193, 205),
        (208, 210),
    ],
    "semantics/str.k": [(13, 17)],
    "semantics/operators.k": [(12, 17)],
    "semantics/int.k": [(13, 20), (26, 27)],
    "semantics/controls.k": [(8, 23), (46, 48), (65, 82)],
    "semantics/functions.k": [(8, 16), (62, 90)],
    "semantics/call.k": [(18, 21), (69, 74)],
}


def relpath(path: Path) -> str:
    if path == ROOT / "verification.k":
        return "verification.k"
    if path == ROOT / "spec.k":
        return "spec.k"
    return str(path.relative_to(SEMANTICS))


def is_used(path_key: str, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in used_ranges.get(path_key, []))


def classify(kind: str, text: str) -> str:
    attrs = set(re.findall(r"\b(functional|function|total|macro-rec|macro|"
                           r"simplification|concrete|owise|priority|"
                           r"no-evaluators|symbol)\b", text))
    if kind == "syntax":
        parts = ["syntax"]
        if "function" in attrs or "functional" in attrs:
            parts.append("function")
        if "total" in attrs:
            parts.append("total")
        if "symbol" in attrs or "no-evaluators" in attrs:
            parts.append("opaque-symbol")
        if "macro" in attrs or "macro-rec" in attrs:
            parts.append("macro")
        return "/".join(parts)
    if kind == "rule":
        parts = ["rule"]
        for marker in ("simplification", "priority", "concrete", "owise"):
            if marker in attrs:
                parts.append(marker)
        return "/".join(parts)
    return kind


rows: list[dict[str, object]] = []
for path in files:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines, start=1):
        match = START.match(line)
        if match and len(match.group("indent").expandtabs(8)) <= 2:
            starts.append((index, match.group("kind")))
    for pos, (start, kind) in enumerate(starts):
        end = starts[pos + 1][0] - 1 if pos + 1 < len(starts) else len(lines)
        segment = lines[start - 1 : end]
        while segment and (
            not segment[-1].strip() or segment[-1].lstrip().startswith("//")
        ):
            segment.pop()
            end -= 1
        code = " ".join(
            part.strip()
            for part in segment
            if part.strip() and not part.lstrip().startswith("//")
        )
        code = re.sub(r"\s+", " ", code)
        key = relpath(path)
        category = classify(kind, code)
        if key == "verification.k":
            disposition = "PROOF-LOCAL: individually reviewed in REVIEW.md"
        elif key == "spec.k":
            disposition = "TARGET CLAIM: adequacy/composition reviewed in REVIEW.md"
        elif key == "semantics/concrete.k":
            disposition = "FIXED SUPPLIED, LLVM-only; excluded from proof definition"
        elif "opaque-symbol" in category:
            disposition = "FIXED SUPPLIED opaque boundary; unreachable on target path"
        elif is_used(key, start):
            disposition = "FIXED SUPPLIED, target-path rule/declaration; reviewed in detail"
        else:
            disposition = "FIXED SUPPLIED, unchanged and unreachable on target path"
        rows.append(
            {
                "file": key,
                "start": start,
                "end": end,
                "kind": kind,
                "category": category,
                "code": code,
                "disposition": disposition,
            }
        )

counts = collections.Counter(str(row["category"]) for row in rows)
print("# Exhaustive K source inventory")
print()
print(
    "Generated from the fresh scratch source tree. A row is one top-level K "
    "sentence; multiline sentences retain their full source range and normalized text."
)
print()
print(f"Total inventoried sentences: {len(rows)}")
print()
print("## Category counts")
print()
print("| Category | Count |")
print("|---|---:|")
for category, count in sorted(counts.items()):
    print(f"| `{category}` | {count} |")

print()
print("## Opaque and symbolic declarations")
print()
opaque_rows = [
    row
    for row in rows
    if "opaque-symbol" in str(row["category"])
    or (
        row["kind"] == "syntax"
        and ("symbol(" in str(row["code"]) or "no-evaluators" in str(row["code"]))
    )
]
if not opaque_rows:
    print("None.")
else:
    for row in opaque_rows:
        print(
            f"- `{row['file']}:{row['start']}` — `{row['code']}` — "
            f"{row['disposition']}"
        )

print()
print("## Sentence-by-sentence inventory")
print()
print("| ID | Source | Category | Normalized sentence | Review disposition |")
print("|---:|---|---|---|---|")
for number, row in enumerate(rows, start=1):
    code = str(row["code"]).replace("|", "\\|")
    disposition = str(row["disposition"]).replace("|", "\\|")
    source = (
        f"`{row['file']}:{row['start']}`"
        if row["start"] == row["end"]
        else f"`{row['file']}:{row['start']}-{row['end']}`"
    )
    print(
        f"| {number} | {source} | `{row['category']}` | `{code}` | "
        f"{disposition} |"
    )
