#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/124-valid-date")
SEMANTICS = ROOT / "reference-semantics"

DECL_RE = re.compile(r"^\s*(configuration|syntax|rule|claim|context)\b")
ATTRIBUTE_RE = re.compile(r"\[([^\]]+)\]")
INTERESTING_ATTRIBUTES = {
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "strict",
    "seqstrict",
    "no-evaluators",
}

# Start lines that participate in execution of solution.mpy. Syntax stanzas are
# marked as relevant when any of their alternatives supplies a used construct.
RELEVANT: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 37, 38, 39, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13, 15, 25, 36, 37, 38, 39, 40, 41, 42, 49,
        124, 125, 126, 127, 130, 131, 132, 145, 152, 157, 158,
        185, 186, 189, 190, 191, 194, 195, 199, 200,
        208, 209, 210, 213, 214, 215, 227, 228, 229,
    },
    "semantics/operators.k": {15, 16, 17},
    "semantics/int.k": {22, 23, 24, 25, 26, 27},
    "semantics/bool.k": {16, 17, 18, 20, 22, 24},
    "semantics/str.k": {13, 14, 15, 16, 25, 26},
    "semantics/subscript.k": {
        16, 17, 18, 21, 22, 23, 27, 28, 35, 37, 40,
        44, 49, 50, 51, 52, 54, 55, 56, 61, 63, 68,
        72, 73, 74, 76, 77, 79, 81, 83, 84, 86, 88,
        90, 91, 93, 96, 97, 99, 102, 103, 105,
        116, 117, 120,
    },
    "semantics/controls.k": {9, 51, 52, 53, 54},
    "semantics/functions.k": {8, 14, 63, 64, 78, 80, 85},
    "semantics/builtins.k": {
        17, 20, 21, 24, 140, 143, 152, 156, 158, 159, 160,
    },
    "semantics/call.k": {19, 20, 21, 31, 32, 69},
}


def source_files() -> list[Path]:
    return [
        SEMANTICS / "semantics.k",
        *sorted((SEMANTICS / "semantics").glob("*.k")),
        ROOT / "verification.k",
        ROOT / "spec.k",
    ]


def relative_name(path: Path) -> str:
    if path.is_relative_to(SEMANTICS):
        return path.relative_to(SEMANTICS).as_posix()
    return path.name


def attributes(block: str) -> str:
    result: set[str] = set()
    code_only = re.sub(r"//.*", "", block)
    for match in ATTRIBUTE_RE.finditer(code_only):
        for raw in match.group(1).split(","):
            value = raw.strip()
            base = value.split("(", 1)[0]
            if (
                base in INTERESTING_ATTRIBUTES
                or base in {"priority", "symbol"}
            ):
                result.add(value)
    return ",".join(sorted(result)) if result else "-"


def summary(block: str) -> str:
    no_comments = re.sub(r"//.*", "", block)
    compact = " ".join(no_comments.split())
    return compact[:220] + ("..." if len(compact) > 220 else "")


def decision(path: Path, line: int, kind: str, block: str) -> tuple[str, str]:
    name = relative_name(path)
    if name == "verification.k":
        return (
            "candidate-extension",
            "REVIEWED_LOCAL: unconditional definitional equation; see REVIEW Stage 5",
        )
    if name == "spec.k":
        return ("target-claim", "REVIEWED_TARGET: adequacy/non-vacuity checked")
    if name == "semantics.k":
        return (
            "supplied-assembly",
            "ACCEPT_SELECTED_SEMANTICS: exact trusted import/assembly file",
        )
    if line in RELEVANT.get(name, set()):
        return (
            "supplied-used",
            "REVIEWED_USED: operational/mathematical behavior checked for this program",
        )
    return (
        "supplied-unreached",
        "ACCEPT_SELECTED_SEMANTICS_UNREACHED: complete declaration/rule pattern absent from solution path",
    )


def main() -> int:
    records: list[dict[str, object]] = []
    for path in source_files():
        lines = path.read_text().splitlines()
        starts = [
            index
            for index, line in enumerate(lines)
            if DECL_RE.match(line)
        ]
        for ordinal, start in enumerate(starts):
            stop = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
            # Do not absorb a later module terminator into the declaration hash.
            for candidate in range(start + 1, stop):
                if re.match(r"^\s*endmodule\b", lines[candidate]):
                    stop = candidate
                    break
            block = "\n".join(lines[start:stop]).rstrip()
            match = DECL_RE.match(lines[start])
            assert match is not None
            kind = match.group(1)
            boundary, result = decision(path, start + 1, kind, block)
            records.append(
                {
                    "file": relative_name(path),
                    "line": start + 1,
                    "kind": kind,
                    "attributes": attributes(block),
                    "boundary": boundary,
                    "decision": result,
                    "sha256_12": hashlib.sha256(block.encode()).hexdigest()[:12],
                    "summary": summary(block),
                }
            )

    counts = collections.Counter(
        (record["boundary"], record["kind"]) for record in records
    )
    print("# Exhaustive K declaration and rule inventory")
    print()
    print(f"Total declarations: {len(records)}")
    print()
    print("Counts by boundary and kind:")
    for (boundary, kind), count in sorted(counts.items()):
        print(f"- {boundary} / {kind}: {count}")
    print()
    print(
        "Each row is keyed by source file, start line, and a hash of the complete "
        "declaration block. `supplied-unreached` means its complete declaration "
        "or rule pattern cannot occur on this submitted program's execution path; "
        "it remains part of the fixed supplied semantics, not a candidate proof "
        "extension."
    )
    print()
    print(
        "| ID | Kind | Attributes | Boundary | Decision | Block SHA-256/12 | Declaration |"
    )
    print("|---|---|---|---|---|---|---|")
    for record in records:
        declaration = str(record["summary"]).replace("|", "\\|")
        print(
            f"| `{record['file']}:{record['line']}` | {record['kind']} | "
            f"`{record['attributes']}` | {record['boundary']} | "
            f"{record['decision']} | `{record['sha256_12']}` | {declaration} |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
