#!/usr/bin/env python3
"""Build an exhaustive sentence inventory for supplied and proof-local K sources."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")

START = re.compile(r"^\s*(configuration|syntax|rule|context|claim|alias)\b")
MODULE = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")
ATTRS = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "strict",
    "seqstrict",
)


def strip_line_comment(line: str) -> str:
    in_string = False
    escaped = False
    index = 0
    while index < len(line) - 1:
        char = line[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "/" and line[index + 1] == "/":
            return line[:index]
        index += 1
    return line


def normalized(lines: list[str]) -> str:
    clean = [strip_line_comment(line).strip() for line in lines]
    return re.sub(r"\s+", " ", " ".join(part for part in clean if part)).strip()


def sentences(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    current_module = "<outside-module>"
    starts: list[tuple[int, str, str]] = []
    module_by_line: dict[int, str] = {}
    for number, line in enumerate(lines, 1):
        module_match = MODULE.match(strip_line_comment(line))
        if module_match:
            current_module = module_match.group(1)
        module_by_line[number] = current_module
        match = START.match(strip_line_comment(line))
        if match:
            starts.append((number, match.group(1), current_module))

    records: list[dict[str, object]] = []
    for index, (line_number, kind, module) in enumerate(starts):
        next_line = starts[index + 1][0] if index + 1 < len(starts) else len(lines) + 1
        # Do not absorb module/end-module/import declarations after the sentence.
        end = next_line - 1
        for candidate in range(line_number + 1, end + 1):
            stripped = strip_line_comment(lines[candidate - 1]).strip()
            if re.match(r"^(?:module|endmodule|imports)\b", stripped):
                end = candidate - 1
                break
        text = normalized(lines[line_number - 1 : end])
        attrs = [attribute for attribute in ATTRS if re.search(rf"\b{re.escape(attribute)}\b", text)]
        records.append(
            {
                "kind": kind,
                "source": str(path),
                "line": line_number,
                "module": module,
                "attrs": ",".join(attrs),
                "text": text,
            }
        )
    return records


def classification(record: dict[str, object]) -> str:
    kind = str(record["kind"])
    attrs = str(record["attrs"]).split(",") if record["attrs"] else []
    if kind == "rule":
        if record["source"] == "/candidate/verification.k" and int(record["line"]) in {
            191,
            209,
            230,
            251,
        }:
            return "operational_bridge"
        if "priority" in attrs:
            return "priority_rule"
        if "simplification" in attrs:
            return "simplification_rule"
        if "concrete" in attrs:
            return "concrete_equation"
        if "owise" in attrs:
            return "owise_rule"
        return "ordinary_rule"
    if kind == "syntax":
        labels = ["syntax_declaration"]
        for attribute in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "macro",
            "strict",
            "seqstrict",
        ):
            if attribute in attrs:
                labels.append(attribute)
        return "+".join(labels)
    return kind


def decision(record: dict[str, object]) -> str:
    source = str(record["source"])
    kind = str(record["kind"])
    line = int(record["line"])
    if source.startswith("/reference/reference-semantics/"):
        return "ACCEPT_SELECTED_SUPPLIED_SEMANTICS"
    if source == "/candidate/spec.k":
        return "CLAIM_SCOPE_REVIEWED"
    if source != "/candidate/verification.k":
        return "REVIEWED"
    if kind == "syntax":
        return "ACCEPT_PROOF_LOCAL_DECLARATION"
    if kind != "rule":
        return "REVIEWED"
    if line in {15, 21, 29, 37, 45}:
        return "ACCEPT_EXACT_TRANSLATED_BODY_DEFINITION"
    if 79 <= line <= 113:
        return "ACCEPT_TRUTHFUL_FINITE_DIGIT_EQUATION"
    if line in {120, 123, 126, 129}:
        return "ACCEPT_DECIMAL_INDEX_EQUATION_ON_POSITIVE_DOMAIN"
    if line == 135:
        return "ACCEPT_RESULT_SPECIFICATION_DEFINITION"
    if 148 <= line <= 157:
        return "ACCEPT_DISJOINT_PROOF_DRIVER_CASE"
    if line in {166, 170, 174, 178}:
        return "ACCEPT_GUARDED_RANGE_CHECK"
    if line in {191, 209, 230, 251}:
        return "REJECT_UNSOUND_BINDING_AND_CONTEXT_BLIND_BRIDGE"
    return "REVIEWED_PROOF_LOCAL"


def main() -> None:
    records: list[dict[str, object]] = []
    for path in ROOTS:
        records.extend(sentences(path))

    for index, record in enumerate(records, 1):
        record["id"] = f"K-{index:04d}"
        record["classification"] = classification(record)
        record["static_decision"] = decision(record)

    fields = [
        "id",
        "kind",
        "classification",
        "source",
        "line",
        "module",
        "attrs",
        "static_decision",
        "text",
    ]
    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(records)

    expected = Counter()
    for path in ROOTS:
        for line in path.read_text().splitlines():
            match = START.match(strip_line_comment(line))
            if match:
                expected[match.group(1)] += 1
    actual = Counter(str(record["kind"]) for record in records)
    if actual != expected:
        raise RuntimeError(f"inventory mismatch expected={expected}, actual={actual}")

    class_counts = Counter(str(record["classification"]) for record in records)
    decision_counts = Counter(str(record["static_decision"]) for record in records)
    attr_counts = Counter()
    for record in records:
        for attribute in str(record["attrs"]).split(","):
            if attribute:
                attr_counts[attribute] += 1

    print(f"sources_inventoried={len(ROOTS)}")
    print(f"records={len(records)}")
    print(f"kind_counts={dict(sorted(actual.items()))}")
    print(f"classification_counts={dict(sorted(class_counts.items()))}")
    print(f"attribute_counts={dict(sorted(attr_counts.items()))}")
    print(f"decision_counts={dict(sorted(decision_counts.items()))}")
    print(f"inventory={OUTPUT}")
    print("unsound_records:")
    for record in records:
        if str(record["static_decision"]).startswith("REJECT_"):
            print(
                f"  {record['id']} {record['source']}:{record['line']} "
                f"{record['static_decision']}"
            )


if __name__ == "__main__":
    main()
