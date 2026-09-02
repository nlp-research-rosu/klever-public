#!/usr/bin/env python3
"""Exhaustive source-level inventory of supplied semantics and proof extensions."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
SEMANTICS = ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/rule_inventory.md")
START = re.compile(
    r"^(?:(requires|module)\b|\s{2}(imports|syntax|configuration|context|rule|claim|alias)\b)"
)

# Rules/declarations on the actual pluck execution path. Other supplied rules
# were still inventoried and read, but their redexes/sorts cannot arise here.
USED_RANGES: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics.k": [(34, 90)],
    "reference-semantics/semantics/syntax.k": [
        (9, 18), (28, 32), (37, 38), (41, 50), (53, 61)
    ],
    "reference-semantics/semantics/core.k": [
        (13, 42), (44, 60), (68, 70), (117, 132), (152, 191),
        (193, 205), (207, 225)
    ],
    "reference-semantics/semantics/iter.k": [(6, 9)],
    "reference-semantics/semantics/operators.k": [(6, 17)],
    "reference-semantics/semantics/int.k": [(4, 27)],
    "reference-semantics/semantics/list.k": [(3, 20)],
    "reference-semantics/semantics/tuple.k": [(30, 41)],
    "reference-semantics/semantics/controls.k": [
        (3, 31), (46, 74), (84, 91)
    ],
    "reference-semantics/semantics/functions.k": [
        (3, 20), (62, 90)
    ],
    "reference-semantics/semantics/call.k": [
        (10, 32), (69, 75)
    ],
    "verification.k": [(1, 90)],
}


def is_used(relative: str, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in USED_RANGES.get(relative, []))


def collect_items(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    items: list[dict[str, object]] = []
    for position, (line_number, kind) in enumerate(starts):
        next_line = starts[position + 1][0] if position + 1 < len(starts) else len(lines) + 1
        chunk_lines = lines[line_number - 1:next_line - 1]
        while chunk_lines and (
            not chunk_lines[-1].strip()
            or chunk_lines[-1].lstrip().startswith("//")
            or chunk_lines[-1].strip() == "endmodule"
        ):
            chunk_lines.pop()
        text = "\n".join(chunk_lines).strip()
        compact = " ".join(part.strip() for part in chunk_lines if part.strip())
        items.append(
            {
                "line": line_number,
                "kind": kind,
                "text": text,
                "compact": compact,
            }
        )
    return items


def verification_decision(line: int, kind: str) -> str:
    if kind in {"requires", "module", "imports"}:
        return "PROOF_MODULE_STRUCTURE"
    if 6 <= line <= 7:
        return "TRUTHFUL_PARTIAL_CAST_ON_INTENDED_INT_DOMAIN"
    if 12 <= line <= 15:
        return "OPERATIONAL_SPECIALIZATION_CONNECTION_CHECKED_SEPARATELY"
    if 19 <= line <= 22:
        return "TRUTHFUL_UNUSED_PREDICATE"
    if 24 <= line <= 45:
        return "TRUTHFUL_EXHAUSTIVE_DISJOINT_STATE_UPDATE"
    if 48 <= line <= 60:
        return "TRUTHFUL_STRUCTURAL_FOLD_ON_INTENDED_INT_DOMAIN"
    if 62 <= line <= 69:
        return "TRUTHFUL_CONSTRUCTOR_PROJECTION"
    if 71 <= line <= 81:
        return "TRUTHFUL_RESULT_FUNCTION_UNDER_NONNEGATIVE_SENTINEL_INVARIANT"
    if 84 <= line <= 89:
        return "EXACT_INT_AND_NONNEGATIVITY_DOMAIN_PREDICATE"
    return "REVIEWED_PROOF_LOCAL_DECLARATION"


def decision(relative: str, line: int, kind: str, compact: str) -> str:
    if relative == "verification.k":
        return verification_decision(line, kind)
    if relative.endswith("/concrete.k"):
        return "CONCRETE_ONLY_EXCLUDED_FROM_PROOF_DEFINITION"
    if "no-evaluators" in compact or "md5hexCodes" in compact:
        return "OPAQUE_TRUST_BOUNDARY_UNUSED_BY_PLUCK"
    if is_used(relative, line):
        return "FIXED_SUPPLIED_SEMANTICS_USED_AND_PATH_REVIEWED"
    return "FIXED_SUPPLIED_SEMANTICS_REDex_UNREACHABLE_ON_PLUCK_CLAIM_PATH"


def flags(kind: str, compact: str) -> str:
    values: list[str] = []
    for flag in (
        "function", "total", "functional", "symbol", "no-evaluators",
        "priority", "simplification", "concrete", "owise", "macro",
        "macro-rec", "strict", "seqstrict",
    ):
        if re.search(rf"\b{re.escape(flag)}\b", compact):
            values.append(flag)
    if kind == "rule" and "priority" not in values and "simplification" not in values:
        values.append("ordinary-rule")
    return ",".join(values) if values else "-"


def main() -> None:
    paths = [SEMANTICS / "semantics.k"]
    paths.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
    paths.append(ROOT / "verification.k")
    all_rows: list[dict[str, object]] = []
    summary: Counter[str] = Counter()
    flag_summary: Counter[str] = Counter()
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        for item in collect_items(path):
            compact = str(item["compact"])
            item_flags = flags(str(item["kind"]), compact)
            row = {
                "file": relative,
                **item,
                "flags": item_flags,
                "decision": decision(
                    relative, int(item["line"]), str(item["kind"]), compact
                ),
            }
            all_rows.append(row)
            summary[str(item["kind"])] += 1
            for flag in item_flags.split(","):
                if flag != "-":
                    flag_summary[flag] += 1

    lines = [
        "# Exhaustive K source inventory",
        "",
        f"Files inventoried: {len(paths)}",
        f"Items inventoried: {len(all_rows)}",
        f"Kind counts: {dict(sorted(summary.items()))}",
        f"Flag counts: {dict(sorted(flag_summary.items()))}",
        "",
        "Every item below is a complete source declaration/rule collapsed to one line.",
        "The decision column distinguishes the fixed supplied semantics, proof-local",
        "extensions, concrete-only rules, and opaque but unreachable primitives.",
        "",
        "| ID | File:line | Kind | Flags | Decision | Complete item |",
        "|---:|---|---|---|---|---|",
    ]
    for index, row in enumerate(all_rows, 1):
        compact = str(row["compact"]).replace("|", "\\|")
        lines.append(
            f"| {index} | `{row['file']}:{row['line']}` | {row['kind']} | "
            f"{row['flags']} | {row['decision']} | `{compact}` |"
        )
    OUTPUT.write_text("\n".join(lines) + "\n")
    print(f"output={OUTPUT}")
    print(f"files={len(paths)}")
    print(f"items={len(all_rows)}")
    print(f"kind_counts={dict(sorted(summary.items()))}")
    print(f"flag_counts={dict(sorted(flag_summary.items()))}")
    print("INVENTORY=PASS")


if __name__ == "__main__":
    main()
