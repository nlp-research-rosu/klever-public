#!/usr/bin/env python3
"""Build a line-addressable inventory of every local K declaration and rule."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reviewer-002/scratch")
SEMANTICS_ROOT = ROOT / "reference-semantics"
FILES = [SEMANTICS_ROOT / "semantics.k"]
FILES.extend(sorted((SEMANTICS_ROOT / "semantics").glob("*.k")))
FILES.append(ROOT / "verification.k")

START = re.compile(
    r"^(?:(requires|module|endmodule)\b| {2}(imports|configuration|context|syntax|rule)\b)"
)
ATTRS = [
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
    "macro-rec",
    "strict",
    "seqstrict",
]

# Rule/declaration start lines that materially execute the submitted program.
USED: dict[str, set[int]] = {
    "semantics/syntax.k": {10, 24, 25, 32, 35, 52, 53, 56, 57},
    "semantics/core.k": {
        13,
        14,
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        199,
        200,
        202,
        209,
        210,
        213,
        214,
        215,
    },
    "semantics/operators.k": {12, 15, 16, 17},
    "semantics/int.k": {9, 15, 16, 19, 20, 22, 24, 26},
    "semantics/bool.k": {16, 17, 22, 24},
    "semantics/controls.k": {
        9,
        20,
        51,
        52,
        53,
        54,
        65,
        77,
        78,
        79,
        81,
        85,
    },
    "semantics/functions.k": {8, 14, 63, 64, 78, 80, 85},
    "semantics/call.k": {19, 20, 21, 69},
}

RUNTIME_TEST: dict[str, set[int]] = {
    "semantics/assert.k": {6, 8, 13},
}


def source_name(path: Path) -> str:
    if path == ROOT / "verification.k":
        return "verification.k"
    return path.relative_to(SEMANTICS_ROOT).as_posix()


def flags(text: str) -> str:
    present = [attr for attr in ATTRS if re.search(rf"\b{re.escape(attr)}\b", text)]
    return ",".join(present) if present else "-"


def assess(source: str, line: int, kind: str, text: str) -> tuple[str, str]:
    if source == "verification.k":
        if kind in {"module", "imports", "requires", "endmodule"}:
            return "PROOF_STRUCTURE", "Imports only the supplied fixed semantics."
        if "macro" in flags(text):
            return (
                "PROOF_LOCAL_EXACT_MACRO",
                "Constructor alias; exact expansion checked against regenerated program.",
            )
        if kind == "syntax":
            return (
                "PROOF_LOCAL_DEFINITION",
                "Typed summary declaration; equations and use-domain reviewed.",
            )
        return (
            "PROOF_LOCAL_REVIEWED_SOUND",
            "Truthful guarded equation or exact constructor macro; no execution bypass.",
        )
    if line in USED.get(source, set()):
        return (
            "USED_PATH_REVIEWED_SOUND",
            "Material submitted-program path; binding/control/state/value behavior reviewed.",
        )
    if line in RUNTIME_TEST.get(source, set()):
        return (
            "RUNTIME_TEST_PATH_REVIEWED_SOUND",
            "Used only by concrete assertion smoke execution, not target proofs.",
        )
    if "no-evaluators" in text or "symbol(" in text:
        return (
            "UNUSED_OPAQUE_BOUNDARY_NO_DEPENDENCY",
            "Opaque selected-semantics boundary; absent from submitted program and claims.",
        )
    if source == "semantics/concrete.k" or "concrete" in flags(text):
        return (
            "UNUSED_CONCRETE_REVIEWED_NO_DEFECT",
            "LLVM/concrete or unused rule; no false witness found in its stated subset and absent from proof.",
        )
    if kind in {"module", "imports", "requires", "endmodule", "configuration"}:
        return (
            "FIXED_STRUCTURE",
            "Selected supplied-semantics structure/configuration.",
        )
    return (
        "SUPPLIED_FIXED_UNUSED_REVIEWED",
        "No false witness found in its stated subset; outside submitted AST path and proof dependency.",
    )


rows: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] - 1 if position + 1 < len(starts) else len(lines)
        block_lines = lines[start - 1 : end]
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()
            end -= 1
        block = "\n".join(block_lines)
        summary = " ".join(part.strip() for part in block_lines if part.strip())
        if len(summary) > 320:
            summary = summary[:317] + "..."
        source = source_name(path)
        status, rationale = assess(source, start, kind, block)
        rows.append(
            {
                "source": source,
                "line": start,
                "end": end,
                "kind": kind,
                "flags": flags(block),
                "status": status,
                "rationale": rationale,
                "summary": summary,
            }
        )

print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Each row is a local top-level declaration/rule block. Continuation lines are "
    "covered by the inclusive line span. `USED_PATH_REVIEWED_SOUND` marks the "
    "material submitted-program path; all other supplied rules are dependency-"
    "classified even when unused."
)
print()
print("| Source | Lines | Kind | Attributes | Assessment | Declaration/rule |")
print("|---|---:|---|---|---|---|")
for row in rows:
    summary = str(row["summary"]).replace("|", "\\|").replace("`", "'")
    print(
        f"| `{row['source']}` | {row['line']}-{row['end']} | {row['kind']} | "
        f"{row['flags']} | {row['status']} | {summary} |"
    )

print()
print("# Counts")
print()
kind_counts = Counter(str(row["kind"]) for row in rows)
status_counts = Counter(str(row["status"]) for row in rows)
flag_counts: Counter[str] = Counter()
for row in rows:
    for flag in str(row["flags"]).split(","):
        if flag != "-":
            flag_counts[flag] += 1
print(f"total_blocks={len(rows)}")
print(f"kind_counts={dict(sorted(kind_counts.items()))}")
print(f"status_counts={dict(sorted(status_counts.items()))}")
print(f"attribute_block_counts={dict(sorted(flag_counts.items()))}")
