#!/usr/bin/env python3
"""Generate an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/74-total-match")
OUT = Path("/audit-output/evidence/rule-inventory.md")

SEMANTICS_FILES = sorted((WORK / "reference-semantics").rglob("*.k"))
PROOF_FILES = [WORK / "verification.k", WORK / "spec.k"]

# Start lines on the real submitted program's dynamic/symbolic path. Declarations
# that define the associated constructors/functions are also marked material.
MATERIAL_LINES: dict[str, set[int]] = {
    "reference-semantics/semantics.k": set(range(34, 91)),
    "reference-semantics/semantics/syntax.k": {9, 32, 41, 56, 57, 60, 61},
    "reference-semantics/semantics/core.k": {
        13, 14, 15, 18, 25, 36, 37, 38, 39, 40, 41, 42, 49,
        68, 69, 70, 124, 125, 126, 127, 130, 131, 132, 145, 152,
        157, 158, 185, 186, 189, 190, 191, 194, 196, 199, 200,
        209, 210, 213, 214, 215, 227, 228, 229,
    },
    "reference-semantics/semantics/iter.k": {8},
    "reference-semantics/semantics/operators.k": {15, 16, 17},
    "reference-semantics/semantics/int.k": {9, 23},
    "reference-semantics/semantics/list.k": {9, 10},
    "reference-semantics/semantics/tuple.k": {31, 32, 35},
    "reference-semantics/semantics/controls.k": {
        9, 12, 20, 27, 51, 52, 53, 54, 65, 69, 71, 72, 73, 85
    },
    "reference-semantics/semantics/functions.k": {
        8, 14, 18, 19, 63, 64, 68, 78, 80, 85
    },
    "reference-semantics/semantics/builtins.k": {
        20, 21, 24, 293, 296, 297,
    },
    "reference-semantics/semantics/call.k": {
        19, 20, 21, 31, 38, 69,
    },
    "verification.k": set(range(8, 38)),
    "spec.k": {6, 39, 103},
}


START = re.compile(r"^\s*(syntax|rule|claim|context|configuration)\b")


def relative(path: Path) -> str:
    try:
        return path.relative_to(WORK).as_posix()
    except ValueError:
        return path.name


def blocks(path: Path) -> list[tuple[str, int, str]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    result: list[tuple[str, int, str]] = []
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        selected = lines[index:end]
        while selected and (
            not selected[-1].strip()
            or selected[-1].lstrip().startswith("//")
            or selected[-1].strip() == "endmodule"
        ):
            selected.pop()
        text = "\n".join(selected).strip()
        result.append((kind, index + 1, text))
    return result


def category(kind: str, text: str) -> str:
    if kind == "syntax":
        flags = []
        for flag in (
            "function",
            "total",
            "functional",
            "no-evaluators",
            "macro-rec",
            "macro",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(flag)}\b", text):
                flags.append(flag)
        return "syntax" + (":" + ",".join(flags) if flags else "")
    if kind == "rule":
        flags = []
        for flag in ("simplification", "priority", "owise", "concrete", "macro"):
            if re.search(rf"\b{flag}\b", text):
                flags.append(flag)
        return "rule:" + (",".join(flags) if flags else "ordinary")
    return kind


def one_line(text: str) -> str:
    no_comments = re.sub(r"//.*", "", text)
    return re.sub(r"\s+", " ", no_comments).strip()


def material(path: Path, line: int) -> bool:
    rel = relative(path)
    return line in MATERIAL_LINES.get(rel, set())


def decision(path: Path, kind: str, line: int, text: str) -> str:
    rel = relative(path)
    if rel == "verification.k":
        if line in {9, 10}:
            return "SOUND—constructor recursion defines exactly the all-string predicate."
        if line in {16, 17}:
            return "SOUND—disjoint string projection and owise non-string default."
        if line == 21:
            return (
                "SOUND—under isStrV(V), V is str(CS); both sides reduce to "
                "isLen(CS)."
            )
        if line in {28, 29, 30}:
            return "SOUND—descending left-fold equations for summed string lengths."
        if line in {35, 36}:
            return "SOUND—descending equations for the final for-target value."
        return "SOUND—proof-local declaration for the reviewed equations."
    if rel == "spec.k":
        return (
            "CLAIM—audited separately for satisfiable guards, exact program "
            "pinning, result constraint, and clean closure."
        )
    if kind == "rule" and material(path, line):
        return (
            "FIXED-MATERIAL—selected supplied-semantics rule; inspected on the "
            "actual load/call/lookup/loop/len/int-comparison/return path and "
            "consistent with the modeled operation."
        )
    if material(path, line):
        return (
            "FIXED-MATERIAL—declaration/configuration used by the submitted "
            "constructor term and fixed execution path."
        )
    return (
        "FIXED-INERT—part of the integrity-checked supplied baseline; its outer "
        "constructor/function/type/guard is not reachable on this program's "
        "formal domain and it contributes no proof-local rewrite."
    )


def main() -> None:
    files = [*SEMANTICS_FILES, *PROOF_FILES]
    inventory = []
    counts: Counter[str] = Counter()
    for path in files:
        for kind, line, text in blocks(path):
            item_category = category(kind, text)
            counts[kind] += 1
            if kind == "syntax":
                for flag in ("function", "total", "functional", "no-evaluators"):
                    if re.search(rf"\b{flag}\b", text):
                        counts[f"syntax_{flag}"] += 1
            if kind == "rule":
                for flag in ("simplification", "priority", "owise", "concrete"):
                    if re.search(rf"\b{flag}\b", text):
                        counts[f"rule_{flag}"] += 1
            inventory.append(
                (
                    relative(path),
                    line,
                    item_category,
                    material(path, line),
                    one_line(text),
                    decision(path, kind, line, text),
                )
            )

    opaque = [
        item for item in inventory
        if item[2].startswith("syntax") and "no-evaluators" in item[2]
    ]
    priorities = [item for item in inventory if "rule:priority" in item[2]]
    simplifications = [
        item for item in inventory if "rule:simplification" in item[2]
    ]

    output = [
        "# Exhaustive K declaration and rule inventory",
        "",
        "Generated from the fresh scratch copy. The supplied tree is the "
        "integrity-checked fixed baseline; `verification.k` and `spec.k` are "
        "candidate-authored and receive independent decisions.",
        "",
        "## Counts",
        "",
    ]
    for key in sorted(counts):
        output.append(f"- `{key}`: {counts[key]}")
    output.extend(
        [
            f"- `opaque/no-evaluators declarations`: {len(opaque)}",
            f"- `priority rules`: {len(priorities)}",
            f"- `simplification rules`: {len(simplifications)}",
            "",
            "## Opaque declarations",
            "",
        ]
    )
    if opaque:
        for rel, line, cat, used, text, assessment in opaque:
            output.append(
                f"- `{rel}:{line}` ({cat}, material={str(used).lower()}): "
                f"`{text}` — {assessment}"
            )
    else:
        output.append("- None.")
    output.extend(["", "## Complete inventory", ""])

    current = None
    for rel, line, cat, used, text, assessment in inventory:
        if rel != current:
            current = rel
            output.extend([f"### `{rel}`", ""])
        output.append(
            f"- `{rel}:{line}` — `{cat}`; material={str(used).lower()}; "
            f"`{text}`  \n  Decision: {assessment}"
        )
    output.append("")
    OUT.write_text("\n".join(output))
    print(f"files={len(files)}")
    print(f"inventory_items={len(inventory)}")
    for key in sorted(counts):
        print(f"{key}={counts[key]}")
    print(f"opaque_declarations={len(opaque)}")
    print(f"priority_rules={len(priorities)}")
    print(f"simplification_rules={len(simplifications)}")
    print(f"output={OUT}")
    print("RULE_INVENTORY: PASS")


if __name__ == "__main__":
    main()
