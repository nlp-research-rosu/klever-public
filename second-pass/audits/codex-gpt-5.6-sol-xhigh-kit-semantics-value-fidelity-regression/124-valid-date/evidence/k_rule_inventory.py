#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory with audit dispositions."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/124-valid-date")
OUTPUT = Path("/audit-output/evidence/16-k-rule-inventory.md")
DIRECTIVE = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim)\b"
)
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim|"
    r"module|endmodule|imports|requires)\b"
)


@dataclass
class Record:
    path: Path
    line: int
    kind: str
    block: str


USED_RULE_LINES: dict[str, set[int]] = {
    "reference-semantics/semantics/core.k": {
        125, 126, 127, 131, 132, 145, 152, 158, 189, 190, 191,
        194, 195, 200, 214, 215, 228, 229,
    },
    "reference-semantics/semantics/functions.k": {
        14, 63, 64, 78, 80, 85,
    },
    "reference-semantics/semantics/call.k": {
        20, 21, 31, 32, 69,
    },
    "reference-semantics/semantics/controls.k": {
        9, 52, 53, 54,
    },
    "reference-semantics/semantics/operators.k": {
        17,
    },
    "reference-semantics/semantics/int.k": {
        22, 23, 24, 25, 26, 27,
    },
    "reference-semantics/semantics/bool.k": {
        17, 18, 20, 22, 24,
    },
    "reference-semantics/semantics/str.k": {
        14, 15, 16, 25, 26, 48, 49, 50, 51, 52, 53, 54,
        56, 57, 58, 59,
    },
    "reference-semantics/semantics/subscript.k": {
        17, 18, 22, 23, 35, 40, 50, 51, 52, 54, 55, 56, 61,
        68, 73, 77, 81, 84, 88, 91, 93, 97, 99, 103, 105,
        117, 120,
    },
    "reference-semantics/semantics/builtins.k": {
        21, 24, 152, 156, 159, 160,
    },
    "reference-semantics/semantics/methods.k": {
        122,
    },
}


def source_files() -> list[Path]:
    semantics = [ROOT / "reference-semantics" / "semantics.k"]
    semantics += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    return semantics + [ROOT / "verification.k", ROOT / "spec.k"]


def records_for(path: Path) -> list[Record]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, text in enumerate(lines):
        match = DIRECTIVE.match(text)
        if match:
            starts.append((index, match.group(1)))
    records: list[Record] = []
    for index, kind in starts:
        end = index + 1
        while end < len(lines) and not BOUNDARY.match(lines[end]):
            end += 1
        block = "\n".join(lines[index:end]).strip()
        records.append(Record(path, index + 1, kind, block))
    return records


def attributes(block: str) -> str:
    names: list[str] = []
    for name in (
        "function",
        "total",
        "functional",
        "simplification",
        "concrete",
        "owise",
        "priority",
        "strict",
        "seqstrict",
        "macro",
        "macro-rec",
        "no-evaluators",
        "symbol",
    ):
        if re.search(rf"\b{re.escape(name)}\b", block):
            names.append(name)
    return ",".join(names) if names else "-"


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def rule_disposition(record: Record) -> tuple[str, str]:
    rel = relative(record.path)
    if rel == "verification.k":
        local = {
            8: (
                "ACCEPT_DERIVED_LEMMA",
                "One-code lexicographic order; exhaustive A<B, A>B, A=B cases.",
            ),
            14: (
                "ACCEPT_PROGRAM_SYNTAX_SUMMARY",
                "Exact closure; independently connected to parsed solution.mpy.",
            ),
            124: (
                "ACCEPT_DEFINITIONAL_ARITHMETIC",
                "Two ASCII digits mapped by elementary base-10 arithmetic.",
            ),
            129: (
                "ACCEPT_DEFINITIONAL_CALENDAR",
                "Exhaustive month-cap expression; invalid months separately rejected.",
            ),
            143: (
                "ACCEPT_RESULT_PREDICATE",
                "Total Boolean equation matching strict mm-dd-yyyy contract.",
            ),
        }
        return local.get(
            record.line,
            ("REVIEW_REQUIRED_UNKNOWN_LOCAL", "Unexpected proof-local rule."),
        )
    if rel == "spec.k":
        return (
            "TARGET_CLAIM",
            "Entry reachability claim; adequacy assessed in REVIEW.md.",
        )
    if rel.startswith("reference-semantics/"):
        if rel.endswith("/concrete.k"):
            return (
                "ACCEPT_SUPPLIED_CONCRETE_ONLY",
                "Trusted supplied LLVM-only baseline; absent from proof definition.",
            )
        if record.line in USED_RULE_LINES.get(rel, set()):
            return (
                "ACCEPT_SUPPLIED_USED_PATH",
                "Trusted fixed rule and manually reviewed on the program/proof path.",
            )
        if "no-evaluators" in record.block or "[concrete]" in record.block:
            return (
                "ACCEPT_SUPPLIED_OPAQUE_UNUSED",
                "Trusted opaque/concrete-only baseline; symbol is unreachable here.",
            )
        return (
            "ACCEPT_SUPPLIED_UNUSED",
            "Trusted fixed baseline; no matching construct is reachable here.",
        )
    return ("UNCLASSIFIED", "Unexpected source.")


def compact(block: str) -> str:
    text = re.sub(r"\s+", " ", block)
    text = text.replace("|", "\\|")
    if len(text) > 260:
        text = text[:257] + "..."
    return text


def main() -> None:
    records: list[Record] = []
    for path in source_files():
        records.extend(records_for(path))
    counts = Counter(record.kind for record in records)
    dispositions: Counter[str] = Counter()
    rows: list[str] = []
    for record in records:
        if record.kind in {"rule", "claim"}:
            disposition, reason = rule_disposition(record)
            dispositions[disposition] += 1
        elif record.kind == "syntax":
            disposition = "DECLARATION_INVENTORIED"
            reason = "Constructor/function attributes recorded; behavior is in its rules."
        elif record.kind == "configuration":
            disposition = "CONFIGURATION_INVENTORIED"
            reason = "Cells and initial values reviewed in REVIEW.md."
        else:
            disposition = "EVALUATION_CONTEXT_INVENTORIED"
            reason = "Evaluation-order context reviewed in REVIEW.md."
        rows.append(
            "| "
            + " | ".join(
                [
                    relative(record.path),
                    str(record.line),
                    record.kind,
                    attributes(record.block),
                    disposition,
                    reason,
                    f"`{compact(record.block)}`",
                ]
            )
            + " |"
        )

    opaque = [
        record
        for record in records
        if record.kind == "syntax" and "no-evaluators" in record.block
    ]
    priority = [
        record
        for record in records
        if record.kind == "rule" and "priority" in record.block
    ]
    simplification = [
        record
        for record in records
        if record.kind == "rule" and "simplification" in record.block
    ]
    total_decls = [
        record
        for record in records
        if record.kind == "syntax" and re.search(r"\btotal\b", record.block)
    ]
    functional_decls = [
        record
        for record in records
        if record.kind == "syntax" and re.search(r"\bfunctional\b", record.block)
    ]

    header = [
        "# Exhaustive K source inventory",
        "",
        "This inventory covers the trusted supplied semantics tree copied into "
        "scratch, the candidate proof-local `verification.k`, and both target "
        "claims in `spec.k`. Generated backend rules are outside the source-level "
        "inventory.",
        "",
        "## Counts",
        "",
        f"- Files: {len(source_files())}",
        f"- Syntax declarations: {counts['syntax']}",
        f"- Configuration declarations: {counts['configuration']}",
        f"- Evaluation contexts: {counts['context']}",
        f"- Ordinary/source rules: {counts['rule']}",
        f"- Claims: {counts['claim']}",
        f"- Total-bearing syntax declarations: {len(total_decls)}",
        f"- Functional-bearing syntax declarations: {len(functional_decls)}",
        f"- Priority rules: {len(priority)}",
        f"- Simplification rules: {len(simplification)}",
        f"- Explicit no-evaluators/opaque declarations: {len(opaque)}",
        "",
        "Rule dispositions: "
        + ", ".join(f"{key}={value}" for key, value in sorted(dispositions.items())),
        "",
        "## Explicit opaque/no-evaluators declarations",
        "",
    ]
    if opaque:
        header.extend(
            f"- `{relative(record.path)}:{record.line}` — `{compact(record.block)}`"
            for record in opaque
        )
    else:
        header.append("- None.")
    header += [
        "",
        "## Complete source record",
        "",
        "| File | Line | Kind | Attributes | Disposition | Audit basis | Source |",
        "|---|---:|---|---|---|---|---|",
    ]
    OUTPUT.write_text("\n".join(header + rows) + "\n", encoding="utf-8")
    print(f"output={OUTPUT}")
    print(
        "counts="
        + ",".join(f"{key}:{counts[key]}" for key in sorted(counts))
    )
    print(f"opaque={len(opaque)} priority={len(priority)}")
    print(
        "dispositions="
        + ",".join(f"{key}:{value}" for key, value in sorted(dispositions.items()))
    )


if __name__ == "__main__":
    main()
