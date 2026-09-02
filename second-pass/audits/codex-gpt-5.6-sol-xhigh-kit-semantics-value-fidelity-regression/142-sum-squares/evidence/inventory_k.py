#!/usr/bin/env python3
"""Create an exhaustive, review-tagged inventory of submitted and supplied K."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import re


WORK = Path("/tmp/audit-work/142-sum-squares")
OUTPUT_JSONL = Path("/audit-output/evidence/k-declaration-inventory.jsonl")
OUTPUT_TSV = Path("/audit-output/evidence/k-declaration-inventory.tsv")
OUTPUT_SUMMARY = Path("/audit-output/evidence/k-declaration-summary.md")

source_paths = sorted((WORK / "reference-semantics").rglob("*.k"))
source_paths += [WORK / "verification.k", WORK / "spec.k"]

declaration_start = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context|alias|macro)\b"
)
attribute_pattern = re.compile(r"\[([^\]]+)\]")


def source_class(path: Path) -> str:
    if "reference-semantics" in path.parts:
        return "SUPPLIED_BASELINE"
    if path.name == "verification.k":
        return "PROOF_LOCAL"
    if path.name == "spec.k":
        return "TARGET_CLAIM"
    raise AssertionError(path)


used_ranges: dict[str, list[tuple[int, int, str]]] = {
    "reference-semantics/semantics/syntax.k": [
        (9, 30, "Expr constructors/evaluation attributes"),
        (32, 39, "comparison and expression-list syntax"),
        (41, 61, "statement/function/module syntax and strictness"),
    ],
    "reference-semantics/semantics/core.k": [
        (13, 42, "Val/ValSeq, closures, scopes, and result sorts"),
        (49, 60, "complete machine configuration"),
        (124, 127, "module and statement sequencing"),
        (130, 154, "Name lookup and scope-chain behavior"),
        (183, 191, "left-to-right call argument evaluation"),
        (193, 205, "literal and truthiness behavior"),
        (207, 219, "operator dispatch and argument sequence helpers"),
    ],
    "reference-semantics/semantics/functions.k": [
        (8, 16, "function closure construction"),
        (62, 66, "parameter binding"),
        (77, 90, "Return, frame pop, and restoration"),
    ],
    "reference-semantics/semantics/call.k": [
        (18, 24, "callee then argument evaluation"),
        (69, 74, "user closure invocation and frame allocation"),
    ],
    "reference-semantics/semantics/operators.k": [
        (12, 17, "binary and comparison dispatch/evaluation"),
    ],
    "reference-semantics/semantics/int.k": [
        (9, 20, "integer +, *, %, and Python modulo"),
        (26, 26, "integer equality"),
    ],
    "reference-semantics/semantics/controls.k": [
        (8, 31, "assignment and augmented assignment"),
        (50, 54, "If branch selection"),
        (62, 74, "For/#loop protocol"),
        (84, 85, "normal loop continuation"),
    ],
    "reference-semantics/semantics/iter.k": [
        (6, 8, "iterator protocol declarations"),
    ],
    "reference-semantics/semantics/list.k": [
        (8, 10, "list iterator cases"),
    ],
    "reference-semantics/semantics/tuple.k": [
        (30, 34, "for-target Name binding"),
    ],
}


proof_local_decisions: dict[int, str] = {
    7: "SOUND: total Boolean list-domain predicate; constructor cases exhaustive",
    8: "SOUND: empty sequence contains only integers",
    9: "SOUND: cons predicate is head-is-Int conjunction tail predicate",
    13: "SOUND: total integer contribution declaration",
    14: "SOUND: divisible-by-3 branch is square",
    16: "SOUND: not-divisible-by-3 and divisible-by-4 branch is cube",
    18: "SOUND: remaining branch is identity; guards partition all integers",
    23: "SOUND: total Val-to-Int projection declaration",
    24: "SOUND: Int-subsort projection is identity",
    25: "SOUND: owise covers non-Int constructors; zero is outside claimed domain",
    30: (
        "SOUND ON GROUND GUARDED DOMAIN: agrees with MPY-INT + whenever "
        "isInt operands are ground; exact-domain symbolic connection did not close"
    ),
    33: (
        "SOUND ON GROUND GUARDED DOMAIN: agrees with MPY-INT * whenever "
        "isInt operands are ground; exact-domain symbolic connection did not close"
    ),
    38: "SOUND: total accumulator summary declaration",
    39: "SOUND: empty suffix returns accumulator",
    40: "SOUND: integer head adds exactly its indexed contribution and descends",
    46: "SOUND: non-Int head case descends; unreachable under entry precondition",
    51: "SOUND: total final-index summary declaration",
    52: "SOUND: empty suffix preserves index",
    53: "SOUND: cons suffix increments index and structurally descends",
}


def relevance(path: Path, line: int) -> str:
    relative = path.relative_to(WORK).as_posix()
    for start, end, reason in used_ranges.get(relative, []):
        if start <= line <= end:
            return f"USED: {reason}"
    if source_class(path) == "SUPPLIED_BASELINE":
        return "UNUSED_BY_SUBMITTED_PROGRAM"
    return "PROOF_OR_CLAIM_LOCAL"


records: list[dict[str, object]] = []
for path in source_paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines, 1):
        match = declaration_start.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (line_number, kind) in enumerate(starts):
        next_line = starts[position + 1][0] if position + 1 < len(starts) else len(lines) + 1
        end_line = next_line - 1
        while end_line >= line_number and (
            not lines[end_line - 1].strip()
            or lines[end_line - 1].lstrip().startswith("//")
            or lines[end_line - 1].strip() == "endmodule"
        ):
            end_line -= 1
        statement = "\n".join(lines[line_number - 1 : end_line]).rstrip()
        attributes = [
            piece.strip()
            for group in attribute_pattern.findall(statement)
            for piece in group.split(",")
        ]
        tags: list[str] = []
        for tag in (
            "function",
            "functional",
            "total",
            "simplification",
            "concrete",
            "owise",
            "macro",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(tag)}\b", statement):
                tags.append(tag)
        if "priority(" in statement:
            tags.append("priority")
        if "symbol(" in statement:
            tags.append("symbol")
        class_name = source_class(path)
        if class_name == "SUPPLIED_BASELINE":
            decision = (
                "ACCEPTED_AT_SELECTED_SEMANTICS_LEVEL: candidate entry is "
                "byte-identical to trusted supplied baseline"
            )
        elif class_name == "PROOF_LOCAL":
            decision = proof_local_decisions.get(
                line_number, "REVIEW_REQUIRED: unmatched proof-local declaration"
            )
        else:
            decision = (
                "TARGET CLAIM: machine closure and adequacy reviewed separately"
            )
        record = {
            "id": len(records) + 1,
            "file": path.relative_to(WORK).as_posix(),
            "start_line": line_number,
            "end_line": end_line,
            "kind": kind,
            "source_class": class_name,
            "tags": tags,
            "attributes": attributes,
            "relevance": relevance(path, line_number),
            "audit_decision": decision,
            "statement": statement,
        }
        records.append(record)

unmatched = [
    record
    for record in records
    if str(record["audit_decision"]).startswith("REVIEW_REQUIRED")
]
if unmatched:
    for record in unmatched:
        print("UNMATCHED", record["file"], record["start_line"], record["statement"])
    raise SystemExit(1)

with OUTPUT_JSONL.open("w", encoding="utf-8") as output:
    for record in records:
        output.write(json.dumps(record, separators=(",", ":")) + "\n")

with OUTPUT_TSV.open("w", encoding="utf-8") as output:
    headers = [
        "id",
        "file",
        "start_line",
        "end_line",
        "kind",
        "source_class",
        "tags",
        "relevance",
        "audit_decision",
        "statement_one_line",
    ]
    output.write("\t".join(headers) + "\n")
    for record in records:
        values = [
            str(record["id"]),
            str(record["file"]),
            str(record["start_line"]),
            str(record["end_line"]),
            str(record["kind"]),
            str(record["source_class"]),
            ",".join(record["tags"]),
            str(record["relevance"]),
            str(record["audit_decision"]),
            re.sub(r"\s+", " ", str(record["statement"])).strip(),
        ]
        output.write("\t".join(value.replace("\t", " ") for value in values) + "\n")

kind_counts = Counter(str(record["kind"]) for record in records)
class_counts = Counter(str(record["source_class"]) for record in records)
tag_counts = Counter(
    tag for record in records for tag in record["tags"]  # type: ignore[union-attr]
)
per_file: dict[str, Counter[str]] = defaultdict(Counter)
for record in records:
    per_file[str(record["file"])][str(record["kind"])] += 1

summary_lines = [
    "# K declaration inventory summary",
    "",
    (
        f"Inventory contains **{len(records)}** declarations. The complete "
        "statement text and per-record review disposition are in "
        "`k-declaration-inventory.jsonl` and `k-declaration-inventory.tsv`."
    ),
    "",
    "## Counts by source class",
    "",
]
for name, count in sorted(class_counts.items()):
    summary_lines.append(f"- {name}: {count}")
summary_lines += ["", "## Counts by declaration kind", ""]
for name, count in sorted(kind_counts.items()):
    summary_lines.append(f"- {name}: {count}")
summary_lines += ["", "## Attribute/tag counts", ""]
for name, count in sorted(tag_counts.items()):
    summary_lines.append(f"- {name}: {count}")
summary_lines += ["", "## Counts by file", "", "| File | Counts |", "|---|---|"]
for file_name, counts in sorted(per_file.items()):
    rendered = ", ".join(f"{name}={count}" for name, count in sorted(counts.items()))
    summary_lines.append(f"| `{file_name}` | {rendered} |")
summary_lines += [
    "",
    "## Interpretation",
    "",
    (
        "Every supplied-semantics declaration is accepted only at the selected "
        "trusted `SUPPLIED_SEMANTICS` level after recursive byte/type integrity "
        "checking. This does not bless any `verification.k` extension. Every "
        "proof-local declaration has an individual decision in the complete "
        "inventory. Opaque/no-evaluator supplied symbols are inventoried but are "
        "unused by `solution.mpy`."
    ),
]
OUTPUT_SUMMARY.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

print(f"records={len(records)}")
print(f"source-class-counts={dict(sorted(class_counts.items()))}")
print(f"kind-counts={dict(sorted(kind_counts.items()))}")
print(f"tag-counts={dict(sorted(tag_counts.items()))}")
print(f"jsonl={OUTPUT_JSONL}")
print(f"tsv={OUTPUT_TSV}")
print(f"summary={OUTPUT_SUMMARY}")
