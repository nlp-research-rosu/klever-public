#!/usr/bin/env python3
"""Exhaustive source-level K declaration/rule inventory for this audit.

The output is TSV so every declaration remains grep-friendly even when its
source text contains K syntax.  Multi-line declarations/rules are represented
as one source-ranged record with whitespace collapsed in the summary field.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


ROOTS = [
    Path("/reference/reference-semantics"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
START = re.compile(
    r"^(requires)(?=\s+\")"
    r"|^\s*(module|endmodule|imports|syntax|configuration|context(?:\s+alias)?|rule|claim)\b"
)

RELEVANT_FIXED = {
    "semantics.k",
    "semantics/syntax.k",
    "semantics/core.k",
    "semantics/iter.k",
    "semantics/operators.k",
    "semantics/int.k",
    "semantics/str.k",
    "semantics/list.k",
    "semantics/tuple.k",
    "semantics/methods.k",
    "semantics/controls.k",
    "semantics/functions.k",
    "semantics/builtins.k",
    "semantics/call.k",
}


def files() -> list[Path]:
    result: list[Path] = []
    for root in ROOTS:
        if root.is_dir():
            result.extend(sorted(root.rglob("*.k")))
        else:
            result.append(root)
    return result


def source_name(path: Path) -> str:
    if path.is_relative_to(Path("/reference/reference-semantics")):
        rel = path.relative_to(Path("/reference/reference-semantics")).as_posix()
        return f"trusted:{rel}"
    return f"candidate:{path.name}"


def disposition(path: Path, start: int, kind: str, text: str) -> str:
    if path.is_relative_to(Path("/reference/reference-semantics")):
        rel = path.relative_to(Path("/reference/reference-semantics")).as_posix()
        relevance = "USED" if rel in RELEVANT_FIXED else "UNUSED"
        return (
            f"{relevance}_SUPPLIED_FIXED_BASELINE:"
            "exact_tree_identity_checked;accepted_as_selected_semantics"
        )
    if path.name == "verification.k":
        if kind == "syntax" and "decimalCodes" in text:
            return "ILLEGITIMATE_RESULT_ORACLE_DECLARATION"
        if start == 28:
            return "ILLEGITIMATE_UNJUSTIFIED_RESULT_ABSTRACTION:opposite_interpretation_witness"
        if start == 132:
            return "OPERATIONAL_BRIDGE:EVIDENCE_GAP_no_bridge_free_connection_definition"
        if start == 210:
            return "ILLEGITIMATE_CIRCULAR_OPERATIONAL_BRIDGE:body_sensitivity_failed"
        if start in (120, 170, 246, 257):
            return "PROGRAM_MACRO_RULE:constructor_identity_checked"
        if kind == "syntax" and "[macro]" in text:
            return "PROGRAM_MACRO_DECLARATION:constructor_identity_checked"
        if start in (31, 60, 61, 62):
            return "DEFINITIONAL_SUMMARY_DEPENDS_ON_UNCONSTRAINED_decimalCodes"
        if start in (74, 77, 78, 79, 81, 82, 84, 85, 87, 88, 105, 107, 108, 109, 112, 113, 114):
            return "SOUND_OR_CONSTRUCTOR_DEFINITION_UNUSED_BY_TARGET"
        if start in (93, 94):
            return "STRING_PROJECTION_ONLY:declared_total_but_equation_covers_only_str"
        if start in (91, 95, 96, 98):
            return "SOUND_DOMAIN_PREDICATE_ON_CONSTRUCTOR_MODEL"
        if kind in ("syntax", "rule"):
            return "SOUND_DEFINITIONAL_MATHEMATICS_OR_STRUCTURAL_HELPER"
        return "MODULE_STRUCTURE"
    if path.name == "spec.k":
        if kind == "claim":
            if start == 6:
                return "AUXILIARY_DIGIT_LOOP:closes;fixed_iteration_plus_math"
            if start == 43:
                return "OUTER_EMPTY:closes_but_operational_bridge_available"
            if start == 84:
                return "CIRCULAR_OUTER_LOOP:exact_candidate_bridge_supplies_poststate"
            if start == 133:
                return "TARGET:real_program_pinned_but_result_oracle_and_outer_bridge"
        return "MODULE_STRUCTURE"
    return "UNCLASSIFIED"


records: list[tuple[str, int, int, str, str]] = []
for path in files():
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for line_number, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            matched_kind = match.group(1) or match.group(2)
            starts.append((line_number, matched_kind.replace(" ", "_")))
    for index, (start, kind) in enumerate(starts):
        end = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start - 1 : end]).strip()
        # Strip trailing comments/blank lines captured before the next declaration.
        block_lines = block.splitlines()
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
            end -= 1
        block = "\n".join(block_lines)
        records.append((source_name(path), start, end, kind, block))

print(
    "id\tsource\tstart_line\tend_line\tkind\tfunction\ttotal\tfunctional"
    "\topaque_symbol\tpriority\tsimplification\tmacro\tdisposition\tsummary"
)
counts: Counter[str] = Counter()
for number, (source, start, end, kind, block) in enumerate(records, 1):
    flags = {
        "function": "[function" in block or ", function" in block,
        "total": "total" in block,
        "functional": "functional" in block,
        "opaque_symbol": "no-evaluators" in block or "symbol(" in block,
        "priority": "priority(" in block,
        "simplification": "simplification" in block,
        "macro": "[macro" in block,
    }
    counts[kind] += 1
    if flags["function"]:
        counts["flag:function"] += 1
    if flags["total"]:
        counts["flag:total"] += 1
    if flags["functional"]:
        counts["flag:functional"] += 1
    if flags["opaque_symbol"]:
        counts["flag:opaque_symbol"] += 1
    if flags["priority"]:
        counts["flag:priority"] += 1
    if flags["simplification"]:
        counts["flag:simplification"] += 1
    if flags["macro"]:
        counts["flag:macro"] += 1
    summary = re.sub(r"\s+", " ", block).replace("\t", " ")
    print(
        "\t".join(
            [
                str(number),
                source,
                str(start),
                str(end),
                kind,
                *(str(flags[name]).lower() for name in (
                    "function",
                    "total",
                    "functional",
                    "opaque_symbol",
                    "priority",
                    "simplification",
                    "macro",
                )),
                disposition(
                    (
                        Path("/reference/reference-semantics")
                        / source.removeprefix("trusted:")
                        if source.startswith("trusted:")
                        else Path("/candidate") / source.removeprefix("candidate:")
                    ),
                    start,
                    kind,
                    block,
                ),
                summary,
            ]
        )
    )

print("# COUNTS")
for key, value in sorted(counts.items()):
    print(f"# {key}={value}")
print(f"# records={len(records)}")
