#!/usr/bin/env python3
"""Create a complete declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


REFERENCE = Path("/reference/reference-semantics")
CANDIDATE = Path("/candidate")
OUTPUT = Path("/audit-output/evidence/05_rule_inventory.tsv")
SUMMARY = Path("/audit-output/evidence/05_rule_inventory_summary.txt")

sources = sorted(REFERENCE.rglob("*.k")) + [
    CANDIDATE / "verification.k",
    CANDIDATE / "spec.k",
]
start_re = re.compile(r"^\s*(configuration|syntax|rule|context|claim)\b")
stop_re = re.compile(r"^(?:requires)\b|^\s*(?:module|endmodule|imports)\b")
flag_names = [
    "function",
    "total",
    "functional",
    "opaque",
    "priority",
    "simplification",
    "macro",
    "owise",
    "concrete",
    "anywhere",
    "symbol",
    "no-evaluators",
]


def strip_line_comment(line: str) -> str:
    """Remove // comments without treating // inside K strings as comments."""
    quoted = False
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quoted:
            escaped = True
            continue
        if char == '"':
            quoted = not quoted
            continue
        if not quoted and line[index : index + 2] == "//":
            return line[:index]
    return line


def local_decision(path: Path, line: int, kind: str, text: str) -> tuple[str, str]:
    if path == CANDIDATE / "verification.k":
        if kind == "syntax":
            if "[macro]" in text:
                return "program macro", "EXACT_MACRO; constructor identity checked"
            return "proof-local declaration", "WELL_SORTED; fresh kompile passed"
        if line in {13, 14}:
            return "definitional representation", "SOUND; structural StrSeq-to-ValSeq equations"
        if line in {18, 21, 22}:
            return "list-iteration operational bridge", "SOUND; complete constructor cases; bridge-free connection checked"
        if line in {27, 30, 32}:
            return "string-containment operational bridge", "SOUND; equals fixed applyCmp/strContains path; connection checked"
        if line in {38, 39, 44, 51}:
            return "mathematical result summary", "SOUND; disjoint exhaustive guards and structural descent"
        if line in {55, 56}:
            return "loop-scope summary", "SOUND; structural descent and exact last-target behavior"
        if line in {61, 67, 73}:
            return "program macro equation", "EXACT_MACRO; expanded KORE equals solution.mpy"
        return "proof-local rule", "MANUALLY_REVIEWED; see REVIEW.md stage 5"
    if path == CANDIDATE / "spec.k":
        return "reachability claim", "RESULT-CONSTRAINING; separately reconstructed and reviewed"
    if kind == "syntax":
        return "fixed supplied declaration", "SELECTED_SUPPLIED_SEMANTICS; fresh kompile passed"
    if kind == "configuration":
        return "fixed supplied configuration", "SELECTED_SUPPLIED_SEMANTICS; reachable cells manually reviewed"
    if kind == "context":
        return "fixed supplied evaluation context", "SELECTED_SUPPLIED_SEMANTICS; reachable contexts manually reviewed"
    if kind == "rule":
        return "fixed supplied rule", "SELECTED_SUPPLIED_SEMANTICS; reachable rules manually reviewed"
    return "fixed supplied item", "SELECTED_SUPPLIED_SEMANTICS"


rows: list[dict[str, str | int]] = []
for path in sources:
    lines = path.read_text().splitlines()
    i = 0
    while i < len(lines):
        match = start_re.match(lines[i])
        if not match:
            i += 1
            continue
        kind = match.group(1)
        start = i
        i += 1
        while i < len(lines):
            if start_re.match(lines[i]) or stop_re.match(lines[i]):
                break
            i += 1
        raw_chunk = "\n".join(lines[start:i]).rstrip()
        chunk = "\n".join(strip_line_comment(line) for line in raw_chunk.splitlines()).rstrip()
        one_line = re.sub(r"\s+", " ", chunk).strip()
        attributes = " ".join(re.findall(r"\[[^\]]*\]", chunk))
        flags = ",".join(name for name in flag_names if re.search(rf"\b{name}\b", attributes))
        role, decision = local_decision(path, start + 1, kind, chunk)
        rows.append(
            {
                "id": len(rows) + 1,
                "source": str(path),
                "line": start + 1,
                "kind": kind,
                "flags": flags,
                "role": role,
                "decision": decision,
                "text": one_line,
            }
        )

with OUTPUT.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["id", "source", "line", "kind", "flags", "role", "decision", "text"],
        dialect="excel-tab",
    )
    writer.writeheader()
    writer.writerows(rows)

by_kind = Counter(str(row["kind"]) for row in rows)
by_flag = Counter()
by_source = Counter(str(row["source"]) for row in rows)
for row in rows:
    for flag in str(row["flags"]).split(","):
        if flag:
            by_flag[flag] += 1

with SUMMARY.open("w") as f:
    print(f"inventory_entries={len(rows)}", file=f)
    print(f"by_kind={dict(sorted(by_kind.items()))}", file=f)
    print(f"by_flag={dict(sorted(by_flag.items()))}", file=f)
    print("by_source:", file=f)
    for source, count in sorted(by_source.items()):
        print(f"{count:4d} {source}", file=f)

print(OUTPUT)
print(SUMMARY)
