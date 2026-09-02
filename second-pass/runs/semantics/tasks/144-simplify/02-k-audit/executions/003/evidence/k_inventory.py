#!/usr/bin/env python3
"""Source-level inventory of every local K declaration, context, rule, and claim."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


SEMANTICS = Path("/reference/reference-semantics")
CANDIDATE_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

START = re.compile(
    r"^\s*(?:"
    r"module\b|endmodule\b|imports\b|"
    r"syntax\b|configuration\b|context\b|rule\b|claim\b|alias\b"
    r")|^requires\s+\""
)


@dataclass
class Record:
    path: Path
    start: int
    end: int
    kind: str
    text: str


def kind_of(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith('requires "'):
        return "requires"
    return stripped.split(maxsplit=1)[0]


def records(path: Path) -> list[Record]:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    result: list[Record] = []
    for position, index in enumerate(starts):
        next_index = starts[position + 1] if position + 1 < len(starts) else len(lines)
        chunk = [
            line for line in lines[index:next_index] if not line.lstrip().startswith("//")
        ]
        while chunk and (not chunk[-1].strip() or chunk[-1].lstrip().startswith("//")):
            chunk.pop()
        text = "\n".join(line.rstrip() for line in chunk)
        result.append(
            Record(
                path=path,
                start=index + 1,
                end=index + len(chunk),
                kind=kind_of(lines[index]),
                text=text,
            )
        )
    return result


def rel(path: Path) -> str:
    if path.is_relative_to(SEMANTICS):
        return "reference-semantics/" + path.relative_to(SEMANTICS).as_posix()
    return path.as_posix()


def classify_rule(text: str) -> str:
    if "[simplification" in text:
        return "simplification"
    if "[concrete" in text:
        return "concrete"
    if "[macro" in text:
        return "macro-rule"
    if "<k>" in text or "<env>" in text or "<heap>" in text or "<scopes>" in text:
        return "operational"
    return "equational"


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


USED_FIXED_RULES = {
    ("semantics/core.k", line)
    for line in (
        118,
        126,
        127,
        131,
        132,
        152,
        158,
        189,
        190,
        191,
        194,
        214,
        215,
    )
} | {
    ("semantics/str.k", 14),
    ("semantics/methods.k", 94),
    ("semantics/tuple.k", 32),
    ("semantics/tuple.k", 50),
    ("semantics/tuple.k", 51),
    ("semantics/tuple.k", 52),
    ("semantics/tuple.k", 55),
    ("semantics/tuple.k", 57),
    ("semantics/functions.k", 63),
    ("semantics/functions.k", 64),
    ("semantics/functions.k", 78),
    ("semantics/functions.k", 85),
    ("semantics/call.k", 16),
    ("semantics/call.k", 20),
    ("semantics/call.k", 21),
    ("semantics/call.k", 24),
    ("semantics/call.k", 32),
    ("semantics/call.k", 69),
    ("semantics/operators.k", 12),
    ("semantics/operators.k", 17),
    ("semantics/int.k", 14),
    ("semantics/int.k", 15),
    ("semantics/int.k", 20),
    ("semantics/int.k", 26),
}


def disposition(record: Record) -> str:
    path = rel(record.path)
    if path == "/candidate/verification.k":
        if record.kind == "syntax" and record.start == 12:
            return "REJECT_UNCONNECTED_RESULT_BEARING_CONSTRUCTORS"
        if record.kind == "rule" and record.start in {15, 18}:
            return "REJECT_UNJUSTIFIED_OPERATIONAL_BRIDGE"
        if record.kind == "syntax" and record.start == 22:
            return "ACCEPT_WRAPPER_DECLARATION"
        if record.kind == "rule" and record.start == 23:
            return "ACCEPT_EXACT_BODY_WRAPPER"
        return "ADMINISTRATIVE"
    if path == "/candidate/spec.k":
        if record.kind == "claim":
            return "TARGET_CLAIM_MATERIALLY_NARROW_ABSTRACT_INPUT_DOMAIN"
        return "ADMINISTRATIVE"
    if record.kind == "rule":
        source_key = (path.removeprefix("reference-semantics/"), record.start)
        if source_key in USED_FIXED_RULES:
            return "ACCEPT_USED_FIXED_RULE_ON_POSITIVE_FRACTION_PATH"
        if path.endswith("semantics/concrete.k"):
            return "ACCEPT_FIXED_CONCRETE_ONLY_NOT_IMPORTED_BY_PROOF"
        return "ACCEPT_FIXED_UNUSED_NO_THEOREM_INFLUENCE"
    if record.kind == "syntax":
        return "ACCEPT_FIXED_DECLARATION"
    if record.kind in {"context", "configuration"}:
        return "ACCEPT_FIXED_EVALUATION_OR_CONFIGURATION"
    return "ADMINISTRATIVE"


def main() -> None:
    paths = [SEMANTICS / "semantics.k", *sorted((SEMANTICS / "semantics").glob("*.k")), *CANDIDATE_FILES]
    all_records: list[Record] = []
    per_file: dict[str, Counter[str]] = {}
    for path in paths:
        file_records = records(path)
        all_records.extend(file_records)
        counter: Counter[str] = Counter(record.kind for record in file_records)
        per_file[rel(path)] = counter

    rule_classes: Counter[str] = Counter()
    attributes: Counter[str] = Counter()
    for record in all_records:
        if record.kind == "rule":
            rule_classes[classify_rule(record.text)] += 1
        if record.kind == "syntax":
            for name in (
                "function",
                "total",
                "functional",
                "symbol",
                "no-evaluators",
                "macro",
                "macro-rec",
                "strict",
                "seqstrict",
            ):
                attributes[name] += len(re.findall(rf"\b{re.escape(name)}\b", record.text))
        if record.kind == "rule":
            for name in ("priority", "owise", "concrete", "simplification"):
                attributes[f"rule:{name}"] += len(re.findall(rf"\b{re.escape(name)}\b", record.text))

    print(f"FILES_INVENTORIED={len(paths)}")
    print(f"TOTAL_RECORDS={len(all_records)}")
    print("PER_FILE_COUNTS")
    for path in paths:
        counter = per_file[rel(path)]
        rendered = " ".join(f"{key}={counter[key]}" for key in sorted(counter))
        print(f"  {rel(path)} {rendered}")
    print(f"RULE_CLASSES={dict(sorted(rule_classes.items()))}")
    print(f"ATTRIBUTE_OCCURRENCES={dict(sorted(attributes.items()))}")

    print("OPAQUE_OR_SYMBOL_DECLARATIONS")
    opaque = [
        record
        for record in all_records
        if record.kind == "syntax" and ("symbol(" in record.text or "no-evaluators" in record.text)
    ]
    for record in opaque:
        print(f"  {rel(record.path)}:{record.start}-{record.end} {one_line(record.text)}")
    print(f"OPAQUE_OR_SYMBOL_COUNT={len(opaque)}")

    print("FUNCTION_TOTAL_FUNCTIONAL_DECLARATIONS")
    function_records = [
        record
        for record in all_records
        if record.kind == "syntax"
        and any(token in record.text for token in ("function", "total", "functional"))
    ]
    for record in function_records:
        print(f"  {rel(record.path)}:{record.start}-{record.end} {one_line(record.text)}")
    print(f"FUNCTION_TOTAL_FUNCTIONAL_RECORD_COUNT={len(function_records)}")

    print("PRIORITY_RULES")
    priority = [record for record in all_records if record.kind == "rule" and "[priority" in record.text]
    for record in priority:
        print(f"  {rel(record.path)}:{record.start}-{record.end} {one_line(record.text)}")
    print(f"PRIORITY_RULE_COUNT={len(priority)}")

    print("SIMPLIFICATION_RULES")
    simplification = [
        record for record in all_records if record.kind == "rule" and "[simplification" in record.text
    ]
    for record in simplification:
        print(f"  {rel(record.path)}:{record.start}-{record.end} {one_line(record.text)}")
    print(f"SIMPLIFICATION_RULE_COUNT={len(simplification)}")

    print("FULL_RECORD_INVENTORY")
    for index, record in enumerate(all_records, 1):
        extra = f" class={classify_rule(record.text)}" if record.kind == "rule" else ""
        print(
            f"{index:04d} {rel(record.path)}:{record.start}-{record.end} "
            f"kind={record.kind}{extra} disposition={disposition(record)} :: {one_line(record.text)}"
        )


if __name__ == "__main__":
    main()
