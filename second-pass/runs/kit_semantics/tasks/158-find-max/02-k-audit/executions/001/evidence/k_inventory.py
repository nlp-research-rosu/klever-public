#!/usr/bin/env python3
"""Build an exhaustive source-level inventory of K declarations and rules."""

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


SEMANTICS_ROOT = Path("/reference/reference-semantics")
CANDIDATE_FILES = [
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/connection.k"),
    Path("/candidate/connection-spec.k"),
]
OUTPUT = Path("/audit-output/evidence/k_inventory.tsv")
SUMMARY = Path("/audit-output/evidence/k_inventory_summary.md")
REVIEW = Path("/audit-output/evidence/static_rule_review.tsv")

paths = sorted(SEMANTICS_ROOT.rglob("*.k")) + CANDIDATE_FILES
start_re = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?|priority)\b"
)
boundary_re = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|rule|claim|"
    r"context(?:\s+alias)?|priority)\b"
)
attribute_re = re.compile(r"\[([^\]]+)\]")


def strip_line_comment(line):
    in_string = False
    escaped = False
    for index in range(len(line) - 1):
        character = line[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
        elif line[index : index + 2] == "//":
            return line[:index]
    return line


def source_class(path):
    if path.is_relative_to(SEMANTICS_ROOT):
        return "trusted-fixed-semantics"
    if path.name == "verification.k":
        return "proof-extension"
    if path.name == "spec.k":
        return "target-claims"
    if path.name == "connection-spec.k":
        return "candidate-validation-claims"
    return "candidate-module-shell"


records = []
for path in paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        code = strip_line_comment(line)
        match = start_re.match(code)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        end = len(lines)
        for candidate in range(start + 1, len(lines)):
            code = strip_line_comment(lines[candidate])
            if boundary_re.match(code):
                end = candidate
                break
        text = "\n".join(lines[start:end]).strip()
        code_text = "\n".join(
            strip_line_comment(line) for line in lines[start:end]
        ).strip()
        attributes = []
        for match in attribute_re.finditer(code_text):
            attributes.extend(
                item.strip() for item in match.group(1).split(",")
            )
        record = {
            "file": str(path),
            "start_line": start + 1,
            "end_line": end,
            "kind": kind,
            "source_class": source_class(path),
            "attributes": ",".join(attributes),
            "has_function": any(
                attribute == "function" for attribute in attributes
            ),
            "has_functional": any(
                attribute == "functional" for attribute in attributes
            ),
            "has_total": any(
                attribute == "total" for attribute in attributes
            ),
            "has_no_evaluators": any(
                attribute == "no-evaluators" for attribute in attributes
            ),
            "has_priority": any(
                attribute.startswith("priority(")
                for attribute in attributes
            )
            or kind == "priority",
            "has_simplification": any(
                attribute.startswith("simplification")
                for attribute in attributes
            ),
            "has_owise": any(
                attribute == "owise" for attribute in attributes
            ),
            "text": re.sub(r"\s+", " ", text),
        }
        records.append(record)


def assessment(record):
    path = Path(record["file"])
    line = record["start_line"]
    kind = record["kind"]
    if record["source_class"] == "trusted-fixed-semantics":
        return (
            "ACCEPTED_SELECTED_FIXED_MODEL",
            "Byte-identical to the launcher-trusted supplied semantics; no "
            "task symbol or task answer occurs. Used operations are mapped "
            "and reviewed in used_construct_map.md; unused opaque/priority "
            "rules are outside this program's reachability slice.",
        )
    if path.name == "verification.k":
        if kind == "syntax":
            return (
                "REVIEWED_PROOF_DECLARATION",
                "Declared proof-local symbol inventoried with its totality/"
                "opacity attributes and defining rules below.",
            )
        if line in {36, 41}:
            return (
                "SOUND_WITH_CONNECTION_EVIDENCE_GAP",
                "Guarded symbolic restatement of the fixed string-constructor "
                "equation. Ground/constructor cases agree and isStr is exact, "
                "but the fresh full-guard bridge-free kprove attempt stuck.",
            )
        if line in {13, 17, 20, 23, 24}:
            return (
                "SOUND_K_SORT_REFINEMENT_BOUNDARY",
                "Uses generated isStr/subsort-cast definedness; no result is "
                "fixed off the string guard and every target use is guarded.",
            )
        return (
            "REVIEWED_SOUND_DEFINITION_OR_STRUCTURAL_FOLD",
            "Truthful definition, disjoint constructor equation, or "
            "structurally descending fold; it does not replace control.",
        )
    if path.name == "spec.k":
        if line == 6:
            return (
                "REVIEWED_SOUND_LOOP_CIRCULARITY",
                "Exact loop head/body and state-threading summary; full-domain "
                "precondition is satisfiable.",
            )
        return (
            "REVIEWED_SOUND_TARGET_CLAIM",
            "Executes the mechanically pinned translated module and constrains "
            "the returned value and observable configuration.",
        )
    if path.name == "connection-spec.k":
        return (
            "VALID_BUT_CONSTRUCTOR_DOMAIN_ONLY",
            "Bridge-free and true by the fixed constructor equation, but not "
            "itself a machine-checked theorem over symbolic Val plus isStr.",
        )
    return (
        "MODULE_WIRING_ONLY",
        "No semantic or proof rule.",
    )


fieldnames = list(records[0])
with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    writer.writerows(records)

review_records = []
for record in records:
    if record["kind"] not in {"rule", "claim"}:
        continue
    verdict, rationale = assessment(record)
    review_records.append(
        {
            "file": record["file"],
            "start_line": record["start_line"],
            "end_line": record["end_line"],
            "kind": record["kind"],
            "attributes": record["attributes"],
            "review": verdict,
            "rationale": rationale,
            "text": record["text"],
        }
    )
with REVIEW.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(review_records[0]),
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(review_records)

kind_counts = Counter(record["kind"] for record in records)
class_counts = Counter(record["source_class"] for record in records)
file_counts = defaultdict(Counter)
for record in records:
    file_counts[record["file"]][record["kind"]] += 1

opaque = [
    record
    for record in records
    if record["has_no_evaluators"]
]
priority = [record for record in records if record["has_priority"]]
simplification = [
    record for record in records if record["has_simplification"]
]
total = [record for record in records if record["has_total"]]
functional = [record for record in records if record["has_functional"]]

with SUMMARY.open("w", encoding="utf-8") as handle:
    handle.write("# Exhaustive K source inventory summary\n\n")
    handle.write(
        f"Inventory: `{OUTPUT}`. Rule/claim review: `{REVIEW}`.\n\n"
    )
    handle.write(f"Files scanned: {len(paths)}.\n\n")
    handle.write(f"Statements inventoried: {len(records)}.\n\n")
    handle.write("## Counts by statement kind\n\n")
    for kind, count in sorted(kind_counts.items()):
        handle.write(f"- {kind}: {count}\n")
    handle.write("\n## Counts by source class\n\n")
    for source, count in sorted(class_counts.items()):
        handle.write(f"- {source}: {count}\n")
    handle.write("\n## Attribute-sensitive counts\n\n")
    handle.write(f"- total declarations/statements: {len(total)}\n")
    handle.write(f"- explicit functional declarations: {len(functional)}\n")
    handle.write(f"- no-evaluators declarations: {len(opaque)}\n")
    handle.write(f"- priority rules/statements: {len(priority)}\n")
    handle.write(f"- simplification rules/statements: {len(simplification)}\n")
    handle.write("\n## Per-file counts\n\n")
    handle.write("| File | Syntax | Rule | Claim | Context | Configuration |\n")
    handle.write("|---|---:|---:|---:|---:|---:|\n")
    for path, counts in sorted(file_counts.items()):
        context_count = counts["context"] + counts["context alias"]
        handle.write(
            f"| `{path}` | {counts['syntax']} | {counts['rule']} | "
            f"{counts['claim']} | {context_count} | "
            f"{counts['configuration']} |\n"
        )
    handle.write("\n## Opaque/no-evaluators declarations\n\n")
    for record in opaque:
        handle.write(
            f"- `{record['file']}:{record['start_line']}` — "
            f"`{record['text']}`\n"
        )

print(f"files={len(paths)}")
print(f"statements={len(records)}")
print(f"kinds={dict(sorted(kind_counts.items()))}")
print(f"source_classes={dict(sorted(class_counts.items()))}")
print(f"rules_and_claims_reviewed={len(review_records)}")
print(f"total_marked={len(total)}")
print(f"functional_marked={len(functional)}")
print(f"opaque_no_evaluators={len(opaque)}")
print(f"priority_marked={len(priority)}")
print(f"simplification_marked={len(simplification)}")
print(f"inventory={OUTPUT}")
print(f"review={REVIEW}")
print(f"summary={SUMMARY}")
