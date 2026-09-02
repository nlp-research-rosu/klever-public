#!/usr/bin/env python3
"""Exhaustive source-level declaration/rule inventory for the audit."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


SEMANTICS_ROOT = Path("/reference/reference-semantics")
CANDIDATE_ROOT = Path("/candidate")

SOURCES = [SEMANTICS_ROOT / "semantics.k"]
SOURCES += sorted((SEMANTICS_ROOT / "semantics").glob("*.k"))
SOURCES += [
    CANDIDATE_ROOT / "verification.k",
    CANDIDATE_ROOT / "bind-base.k",
    CANDIDATE_ROOT / "bind-spec.k",
    CANDIDATE_ROOT / "loop-base.k",
    CANDIDATE_ROOT / "loop-spec.k",
    CANDIDATE_ROOT / "spec.k",
]

START = re.compile(
    r"^(?:(requires|module|endmodule)\b|  "
    r"(imports|configuration|syntax|context|rule|claim)\b)"
)

# Line intervals whose fixed-semantics rules/declarations are reachable from
# solution.mpy on List[int] entry states (plus module loading of that program).
USED_RANGES: dict[str, list[tuple[int, int]]] = {
    "semantics.k": [(34, 90)],
    "semantics/syntax.k": [(9, 61)],
    "semantics/core.k": [
        (12, 60),
        (117, 121),
        (123, 127),
        (129, 181),
        (183, 205),
        (207, 225),
    ],
    "semantics/controls.k": [
        (8, 18),
        (33, 54),
        (62, 75),
        (93, 108),
    ],
    "semantics/functions.k": [(8, 20), (62, 90)],
    "semantics/call.k": [(15, 32), (52, 75)],
    "semantics/list.k": [(8, 20), (52, 55)],
    "semantics/tuple.k": [(30, 41)],
    "semantics/operators.k": [(14, 17)],
    "semantics/int.k": [(22, 27)],
    "semantics/subscript.k": [(6, 40)],
    "semantics/str.k": [(12, 17)],
    "semantics/iter.k": [(6, 8)],
}


def relative(path: Path) -> str:
    if path.is_relative_to(SEMANTICS_ROOT):
        return path.relative_to(SEMANTICS_ROOT).as_posix()
    return f"candidate/{path.name}"


def reachable(path: Path, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in USED_RANGES.get(relative(path), []))


def disposition(path: Path, line: int, kind: str) -> str:
    rel = relative(path)
    if rel.startswith("candidate/"):
        if path.name == "verification.k" and kind == "rule":
            if line == 13:
                return "DERIVED_SORT_LEMMA_REVIEWED_SOUND"
            if line in (56, 71):
                return "OPERATIONAL_BRIDGE_SEPARATE_CONNECTION_PROVED"
            return "DEFINITIONAL_EQUATION_REVIEWED_SOUND_ON_GUARDED_DOMAIN"
        if kind == "claim":
            return "POSITIVE_REACHABILITY_CLAIM_REVIEWED"
        if kind in {"syntax", "configuration", "context"}:
            return "PROOF_LOCAL_DECLARATION_REVIEWED"
        return "PROOF_MODULE_WIRING_REVIEWED"
    if kind == "rule":
        if reachable(path, line):
            return "FIXED_RULE_REVIEWED_SOUND_ON_INTENDED_INT_LIST_PATH"
        return "NO_INTENDED_PATH_MATCH;UNREACHED_FIXED_RULE_NOT_GLOBALLY_BLESSED"
    if kind == "context":
        if reachable(path, line):
            return "FIXED_EVALUATION_CONTEXT_REVIEWED_ON_INTENDED_PATH"
        return "NO_INTENDED_PATH_MATCH;UNREACHED_CONTEXT"
    if kind in {"syntax", "configuration"}:
        if reachable(path, line):
            return "FIXED_DECLARATION_USED_AND_REVIEWED"
        return "FIXED_DECLARATION_UNUSED_BY_SUBMITTED_PROGRAM"
    return "SOURCE_ASSEMBLY_OR_MODULE_WIRING_REVIEWED"


def statements(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, text in enumerate(lines, 1):
        match = START.match(text)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for position, (line, kind) in enumerate(starts):
        next_line = starts[position + 1][0] if position + 1 < len(starts) else len(lines) + 1
        block = "\n".join(lines[line - 1 : next_line - 1]).rstrip()
        yield line, kind, block


def main() -> int:
    rows = []
    for path in SOURCES:
        for line, kind, block in statements(path):
            code_block = "\n".join(
                source_line.split("//", 1)[0] for source_line in block.splitlines()
            )
            attributes = sorted(
                {
                    value
                    for group in re.findall(r"\[([^\]]+)\]", code_block)
                    for value in re.split(r"\s*,\s*|\s+", group)
                    if value
                }
            )
            normalized = " ".join(
                part.strip()
                for part in code_block.splitlines()
                if part.strip() and not part.lstrip().startswith("//")
            )
            rows.append(
                {
                    "file": relative(path),
                    "line": line,
                    "kind": kind,
                    "attributes": ",".join(attributes) or "-",
                    "disposition": disposition(path, line, kind),
                    "sha256": hashlib.sha256(block.encode()).hexdigest(),
                    "source": normalized,
                }
            )

    kind_counts = Counter(row["kind"] for row in rows)
    disposition_counts = Counter(row["disposition"] for row in rows)
    print(f"files={len(SOURCES)}")
    print(f"entries={len(rows)}")
    print(f"kind_counts={dict(sorted(kind_counts.items()))}")
    print(f"disposition_counts={dict(sorted(disposition_counts.items()))}")
    print(
        "opaque_or_no_evaluators="
        f"{sum('no-evaluators' in row['attributes'] for row in rows)}"
    )
    print(
        "total_declarations="
        f"{sum('total' in row['attributes'] for row in rows)}"
    )
    print(
        "functional_declarations="
        f"{sum('functional' in row['attributes'] for row in rows)}"
    )
    print(
        "simplification_rules="
        f"{sum('simplification' in row['attributes'] for row in rows)}"
    )
    print(
        "priority_entries="
        f"{sum(any(a.startswith('priority') for a in row['attributes'].split(',')) for row in rows)}"
    )
    print()
    print(
        "ID\tFILE\tLINE\tKIND\tATTRIBUTES\tDISPOSITION\tBLOCK_SHA256\tNORMALIZED_SOURCE"
    )
    for index, row in enumerate(rows, 1):
        print(
            f"I{index:04d}\t{row['file']}\t{row['line']}\t{row['kind']}\t"
            f"{row['attributes']}\t{row['disposition']}\t{row['sha256']}\t"
            f"{row['source']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
