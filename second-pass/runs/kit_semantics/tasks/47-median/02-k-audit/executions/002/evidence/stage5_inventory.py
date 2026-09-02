#!/usr/bin/env python3
"""Lexical source inventory cross-checked against the fresh K compilation."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/median47")
SEMANTICS = SCRATCH / "reference-semantics"
SOURCE_PATHS = [
    SEMANTICS / "semantics.k",
    *sorted((SEMANTICS / "semantics").glob("*.k")),
    SCRATCH / "program.k",
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]
START = re.compile(
    r"^\s*(syntax|configuration|rule|claim|context(?:\s+alias)?|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s*(syntax|configuration|rule|claim|context(?:\s+alias)?|alias|"
    r"module|endmodule|imports)\b"
)


@dataclass
class Statement:
    path: Path
    line: int
    kind: str
    text: str

    @property
    def attrs(self) -> tuple[str, ...]:
        attributes: list[str] = []
        for group in re.findall(r"\[([^\]]+)\]", self.text):
            attributes.extend(part.strip() for part in group.split(","))
        return tuple(attributes)


def statements(path: Path) -> list[Statement]:
    lines = path.read_text().splitlines()
    found: list[Statement] = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        end = index + 1
        while end < len(lines) and not BOUNDARY.match(lines[end]):
            if not lines[end].strip():
                break
            end += 1
        block = "\n".join(line.rstrip() for line in lines[index:end])
        found.append(Statement(path, index + 1, kind, block))
        index = max(end, index + 1)
    return found


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def rule_class(statement: Statement) -> str:
    attrs = statement.attrs
    classes: list[str] = []
    if any(attr.startswith("simplification") for attr in attrs):
        classes.append("simplification")
    if "concrete" in attrs:
        classes.append("concrete")
    if any(attr.startswith("priority(") for attr in attrs):
        classes.append("priority")
    if "owise" in attrs:
        classes.append("owise")
    if "anywhere" in attrs:
        classes.append("anywhere")
    if not classes:
        classes.append("ordinary")
    return "+".join(classes)


def main() -> int:
    all_statements = [
        statement
        for path in SOURCE_PATHS
        for statement in statements(path)
    ]
    print(
        "INVENTORY_HEADER\tpath\tline\tkind\tclassification\tattributes\tstatement"
    )
    counters: dict[str, Counter[str]] = defaultdict(Counter)
    opaque: list[str] = []
    functions: list[str] = []
    totals: list[str] = []
    functionals: list[str] = []
    priority_rules: list[str] = []
    simplification_rules: list[str] = []
    for statement in all_statements:
        relative = statement.path.relative_to(SCRATCH).as_posix()
        attrs = statement.attrs
        if statement.kind == "rule":
            classification = rule_class(statement)
        elif statement.kind == "syntax":
            flags = [
                flag
                for flag in (
                    "function",
                    "functional",
                    "total",
                    "macro",
                    "macro-rec",
                    "strict",
                    "seqstrict",
                    "no-evaluators",
                )
                if any(flag in attr for attr in attrs)
            ]
            classification = "+".join(flags) if flags else "data-syntax"
        else:
            classification = statement.kind
        print(
            "ITEM\t"
            f"{relative}\t{statement.line}\t{statement.kind}\t"
            f"{classification}\t{','.join(attrs)}\t{one_line(statement.text)}"
        )
        counters[relative][statement.kind] += 1
        location = f"{relative}:{statement.line}"
        if statement.kind == "syntax":
            if any("function" == attr for attr in attrs):
                functions.append(location)
            if "total" in attrs:
                totals.append(location)
            if "functional" in attrs:
                functionals.append(location)
            if "no-evaluators" in attrs:
                opaque.append(location)
        if statement.kind == "rule":
            if any(attr.startswith("priority(") for attr in attrs):
                priority_rules.append(location)
            if any(attr.startswith("simplification") for attr in attrs):
                simplification_rules.append(location)

    for relative, count in sorted(counters.items()):
        print(
            f"FILE_SUMMARY\t{relative}\t"
            + "\t".join(f"{kind}={number}" for kind, number in sorted(count.items()))
        )
    total_counts = Counter(statement.kind for statement in all_statements)
    print(f"TOTAL_STATEMENTS={len(all_statements)}")
    print(f"TOTAL_BY_KIND={dict(sorted(total_counts.items()))}")
    print(f"FUNCTION_DECLARATIONS={len(functions)} locations={functions}")
    print(f"TOTAL_DECLARATIONS={len(totals)} locations={totals}")
    print(f"FUNCTIONAL_DECLARATIONS={len(functionals)} locations={functionals}")
    print(f"OPAQUE_NO_EVALUATORS={len(opaque)} locations={opaque}")
    print(f"PRIORITY_RULES={len(priority_rules)} locations={priority_rules}")
    print(
        f"SIMPLIFICATION_RULES={len(simplification_rules)} "
        f"locations={simplification_rules}"
    )

    all_rules = (
        SCRATCH / "audit-verification-kompiled" / "allRules.txt"
    ).read_text().splitlines()
    compiled_local: list[tuple[str, int]] = []
    for line in all_rules:
        match = re.search(r" (/tmp/audit-work/median47/[^:]+):(\d+):\d+$", line)
        if match:
            path = Path(match.group(1)).relative_to(SCRATCH).as_posix()
            compiled_local.append((path, int(match.group(2))))
    compiled_counts = Counter(path for path, _ in compiled_local)
    print(f"FRESH_COMPILED_LOCAL_RULE_ENTRIES={len(compiled_local)}")
    print(f"FRESH_COMPILED_RULES_BY_FILE={dict(sorted(compiled_counts.items()))}")

    source_rule_locations = {
        (statement.path.relative_to(SCRATCH).as_posix(), statement.line)
        for statement in all_statements
        if statement.kind in {"rule", "context", "context alias"}
        and statement.path.name != "spec.k"
    }
    compiled_locations = set(compiled_local)
    missing_from_compiled = sorted(source_rule_locations - compiled_locations)
    print(
        "SOURCE_RULE_OR_CONTEXT_LOCATIONS_NOT_DIRECTLY_IN_ALLRULES="
        f"{missing_from_compiled}"
    )

    semantics_text = "\n".join(
        path.read_text()
        for path in SOURCE_PATHS
        if "reference-semantics" in path.as_posix()
    )
    local_text = (SCRATCH / "program.k").read_text() + (
        SCRATCH / "verification.k"
    ).read_text() + (SCRATCH / "spec.k").read_text()
    print(
        f"SEMANTICS_CONTAINS_CASE_INSENSITIVE_MEDIAN="
        f"{'median' in semantics_text.lower()}"
    )
    print(
        f"PROOF_LOCAL_CONTAINS_MEDIAN={'median' in local_text.lower()} "
        "(expected: program binding and claim labels)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
