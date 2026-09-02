#!/usr/bin/env python3
"""Emit an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
DECL = re.compile(r"^(?P<indent>\s*)(?P<kind>configuration|syntax|context|rule|claim|alias)\b")
MODULE = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")
ENDMODULE = re.compile(r"^\s*endmodule\b")


@dataclass
class Record:
    path: Path
    module: str
    line: int
    kind: str
    text: str


def source_files() -> list[Path]:
    fixed = sorted((ROOT / "reference-semantics").rglob("*.k"))
    local = [ROOT / "verification.k", ROOT / "spec.k"]
    return fixed + local


def records(path: Path) -> list[Record]:
    lines = path.read_text().splitlines()
    result: list[Record] = []
    module = "<outside-module>"
    index = 0
    while index < len(lines):
        line = lines[index]
        module_match = MODULE.match(line)
        if module_match:
            module = module_match.group(1)
            index += 1
            continue
        if ENDMODULE.match(line):
            module = "<outside-module>"
            index += 1
            continue
        match = DECL.match(line)
        if not match:
            index += 1
            continue
        indent = len(match.group("indent"))
        kind = match.group("kind")
        start = index
        index += 1
        while index < len(lines):
            candidate = lines[index]
            if MODULE.match(candidate) or ENDMODULE.match(candidate):
                break
            next_match = DECL.match(candidate)
            if next_match and len(next_match.group("indent")) <= indent:
                break
            index += 1
        block = "\n".join(lines[start:index]).rstrip()
        result.append(Record(path, module, start + 1, kind, block))
    return result


def flags(text: str) -> str:
    checks = [
        ("function", r"\bfunction\b"),
        ("total", r"\btotal\b"),
        ("functional", r"\bfunctional\b"),
        ("macro", r"\bmacro\b"),
        ("simplification", r"\bsimplification\b"),
        ("concrete", r"\bconcrete\b"),
        ("priority", r"\bpriority\s*\("),
        ("opaque", r"\bopaque\b"),
        ("anywhere", r"\banywhere\b"),
        ("owise", r"\bowise\b"),
        ("requires", r"\brequires\b"),
        ("ensures", r"\bensures\b"),
    ]
    return ",".join(label for label, pattern in checks if re.search(pattern, text)) or "-"


def decision(record: Record) -> str:
    rel = record.path.relative_to(ROOT).as_posix()
    if rel.startswith("reference-semantics/"):
        if record.kind in {"rule", "context", "configuration"}:
            return (
                "FIXED_SUPPLIED_BASELINE; exact trusted-tree match; "
                "accept at selected-semantics trust boundary subject to used-path review"
            )
        return "FIXED_SUPPLIED_DECLARATION; exact trusted-tree match"
    if rel == "spec.k":
        return "CLAIM; adequacy/result/non-vacuity decision in REVIEW stage 4/6"
    line = record.line
    if record.kind == "syntax" and line == 15:
        return "REJECT: opaque musicCodes has no concrete-string encoding equations"
    if record.kind == "rule" and line == 28:
        return (
            "REJECT: proof-only split operational bridge lacks bridge-free theorem "
            "and suppresses real split allocation"
        )
    if record.kind == "rule" and line in {20, 21, 23, 25}:
        return "CONDITIONAL ghost-iterator equation; truthful only for unconnected abstraction"
    if record.kind == "rule" and line in {34, 35, 37, 39}:
        return "ACCEPT ordinary recursive duration summary over Music constructors"
    if record.kind == "rule" and line in {44, 45, 47, 49}:
        return "ACCEPT ordinary recursive final-note summary over Music constructors"
    if record.kind == "rule" and line in {55, 63, 72, 76}:
        return "ACCEPT syntax macro; constructor-level KAST comparison recorded"
    if record.kind == "rule" and line == 89:
        return (
            "CONDITIONAL derived loop lemma; independently closes against BASE, "
            "but its domain begins at ghost musicIter"
        )
    return "LOCAL_DECLARATION; see REVIEW stage 5 classification"


def main() -> int:
    all_records: list[Record] = []
    for path in source_files():
        all_records.extend(records(path))

    counts = Counter()
    print("INVENTORY_FORMAT=ID|SOURCE|MODULE|LINE|KIND|FLAGS|DECISION|NORMALIZED_TEXT")
    for number, record in enumerate(all_records, 1):
        rel = record.path.relative_to(ROOT).as_posix()
        normalized = " ".join(
            segment.strip()
            for segment in record.text.splitlines()
            if segment.strip() and not segment.lstrip().startswith("//")
        )
        record_flags = flags(record.text)
        record_decision = decision(record)
        print(
            f"K{number:04d}|{rel}|{record.module}|{record.line}|{record.kind}|"
            f"{record_flags}|{record_decision}|{normalized}"
        )
        counts[(rel, record.kind)] += 1

    print("SUMMARY")
    for (rel, kind), count in sorted(counts.items()):
        print(f"COUNT|{rel}|{kind}|{count}")
    print(f"TOTAL_RECORDS={len(all_records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
