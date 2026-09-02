#!/usr/bin/env python3
"""Build an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/audit73")
OUTPUT = Path("/audit-output/evidence/k-rule-inventory.md")
START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|rule|context|claim|alias)\b"
)

USED_BASELINE_FILES = {
    "reference-semantics/semantics.k",
    "reference-semantics/semantics/syntax.k",
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/call.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/int.k",
    "reference-semantics/semantics/subscript.k",
    "reference-semantics/semantics/builtins.k",
}


def proof_assessment(line: int, kind: str) -> str:
    if kind == "syntax":
        if line in {7, 34, 43, 47}:
            return "proof-local macro declaration; manually duplicates submitted AST"
        if line == 52:
            return "definitional total mismatch-count summary"
        if line in {64, 65, 88}:
            return "synthetic proof-control declaration"
        if line in {118, 124}:
            return "definitional total result/precondition summary"
    if kind == "rule":
        if line in {8, 35}:
            return "AST macro equation matches submitted source text; no mechanical program link"
        if line in {44, 48}:
            return "closure macro equation; synthetic entry value, not loaded from solution.mpy"
        if line in {53, 55}:
            return "mathematically valid interval recurrence; disjoint guards, descent by width"
        if line in {73, 79}:
            return (
                "ILLEGITIMATE operational bridge: priority rewrite replaces fixed call/body "
                "execution; no bridge-free connection theorem; body-sensitivity test passes wrongly"
            )
        if line == 90:
            return "synthetic wrapper recurrence; result-correct for list heap, but bypasses body"
        if line == 101:
            return "synthetic helper base case; mathematically valid"
        if line == 104:
            return "synthetic helper recurrence; valid in-bounds math, but bypasses body"
        if line == 115:
            return "valid mismatch-bit addition continuation"
        if line in {119, 121}:
            return "truthful definitional equation for synthetic target answer"
        if line in {125, 126}:
            return "satisfiable domain predicate; guards helper indices but not a program link"
    return "proof-local declaration reviewed; see Stage 5 discussion"


def spec_assessment(line: int) -> str:
    if line == 6:
        return "closes only by importing the same public operational bridge; not a connection theorem"
    if line == 13:
        return "closes only by importing the same helper operational bridge; not a connection theorem"
    if line == 23:
        return "result-constraining theorem about synthetic #targetCall, not solution.mpy execution"
    return "spec structure"


def source_assessment(rel: str, line: int, kind: str, text: str) -> str:
    if rel == "verification.k":
        return proof_assessment(line, kind)
    if rel == "spec.k":
        return spec_assessment(line)
    if rel.startswith("reference-semantics/"):
        relevance = "used construct path" if rel in USED_BASELINE_FILES else "unused by submitted program"
        opaque = "; declared opaque/total primitive" if "no-evaluators" in text else ""
        return (
            "ACCEPTED fixed SUPPLIED_SEMANTICS baseline (byte-identical trusted tree); "
            f"{relevance}{opaque}"
        )
    return "unclassified"


def records_for(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    records: list[dict[str, object]] = []
    rel = path.relative_to(ROOT).as_posix()
    for pos, (start, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        raw_lines = []
        for line in lines[start:end]:
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                continue
            raw_lines.append(stripped)
        text = " ".join(raw_lines)
        text = re.sub(r"\s+", " ", text)
        attrs = sorted(
            {
                name
                for name in (
                    "function",
                    "total",
                    "functional",
                    "simplification",
                    "priority",
                    "macro",
                    "symbol",
                    "no-evaluators",
                    "owise",
                    "anywhere",
                )
                if re.search(rf"\b{re.escape(name)}\b", text)
            }
        )
        records.append(
            {
                "file": rel,
                "line": start + 1,
                "kind": kind,
                "attrs": ",".join(attrs) if attrs else "-",
                "text": text,
                "assessment": source_assessment(rel, start + 1, kind, text),
            }
        )
    return records


def main() -> int:
    paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])
    records = [record for path in paths for record in records_for(path)]
    counts = Counter(str(record["kind"]) for record in records)
    attr_counts: Counter[str] = Counter()
    for record in records:
        if record["attrs"] != "-":
            attr_counts.update(str(record["attrs"]).split(","))

    output = [
        "# Exhaustive K declaration and rule inventory",
        "",
        "Generated by reviewer-authored `k_rule_inventory.py`. Every declaration start",
        "(`configuration`, `syntax`, `context`, `rule`, `claim`, module/import boundary)",
        "in the supplied semantics, proof extension, and spec is listed below.",
        "",
        f"- Total records: {len(records)}",
        f"- Kind counts: {dict(sorted(counts.items()))}",
        f"- Attribute counts: {dict(sorted(attr_counts.items()))}",
        "- `simplification` declarations found: "
        f"{attr_counts.get('simplification', 0)}",
        "- `functional` declarations found: "
        f"{attr_counts.get('functional', 0)}",
        "",
        "| # | Location | Kind | Attributes | Normalized declaration/rule | Assessment |",
        "|---:|---|---|---|---|---|",
    ]
    for index, record in enumerate(records, 1):
        text = str(record["text"]).replace("|", "&#124;")
        assessment = str(record["assessment"]).replace("|", "&#124;")
        output.append(
            f"| {index} | `{record['file']}:{record['line']}` | {record['kind']} | "
            f"{record['attrs']} | `{text}` | {assessment} |"
        )
    OUTPUT.write_text("\n".join(output) + "\n")

    print(f"OUTPUT: {OUTPUT}")
    print(f"TOTAL_RECORDS: {len(records)}")
    print(f"KIND_COUNTS: {dict(sorted(counts.items()))}")
    print(f"ATTRIBUTE_COUNTS: {dict(sorted(attr_counts.items()))}")
    print(f"SIMPLIFICATION_COUNT: {attr_counts.get('simplification', 0)}")
    print(f"FUNCTIONAL_COUNT: {attr_counts.get('functional', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
