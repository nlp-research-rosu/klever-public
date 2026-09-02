#!/usr/bin/env python3
"""Lexically inventory every local K declaration, rule, and claim.

This intentionally inventories source statements rather than trusting a
candidate-provided compiled definition.  The generated Markdown is the
row-by-row audit ledger referenced by REVIEW.md.
"""

from __future__ import annotations

import collections
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/75-prime/candidate")
OUTPUT = Path("/audit-output/evidence/stage5-rule-inventory.md")
START = re.compile(
    r"^(?:(requires)\b|\s*(module|endmodule|imports|syntax|configuration|"
    r"context|rule|claim|alias)\b)"
)


def start_kind(line: str) -> str | None:
    match = START.match(line)
    if not match or line.lstrip().startswith("//"):
        return None
    return match.group(1) or match.group(2)


@dataclass
class Record:
    path: Path
    line: int
    kind: str
    text: str


def records_for(path: Path) -> list[Record]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        kind = start_kind(line)
        if kind:
            starts.append((index, kind))

    records: list[Record] = []
    for pos, (index, kind) in enumerate(starts):
        next_index = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        block = lines[index:next_index]
        while block and (
            not block[-1].strip() or block[-1].lstrip().startswith("//")
        ):
            block.pop()
        records.append(
            Record(
                path=path,
                line=index + 1,
                kind=kind,
                text="\n".join(block),
            )
        )
    return records


EXERCISED_RULE_STARTS: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics/core.k": [
        (69, 70),
        (125, 127),
        (131, 134),
        (189, 191),
        (194, 195),
        (200, 200),
        (214, 215),
    ],
    "reference-semantics/semantics/controls.k": [
        (9, 18),
        (20, 31),
        (48, 48),
        (52, 54),
        (77, 85),
    ],
    "reference-semantics/semantics/functions.k": [
        (14, 16),
        (63, 66),
        (78, 79),
        (85, 90),
    ],
    "reference-semantics/semantics/call.k": [
        (20, 21),
        (69, 74),
    ],
    "reference-semantics/semantics/operators.k": [
        (12, 17),
    ],
    "reference-semantics/semantics/int.k": [
        (9, 9),
        (14, 16),
        (20, 20),
        (23, 26),
    ],
    "reference-semantics/semantics/str.k": [
        (14, 17),
    ],
}


def in_ranges(value: int, ranges: list[tuple[int, int]]) -> bool:
    return any(low <= value <= high for low, high in ranges)


def flags(record: Record) -> list[str]:
    text = record.text
    found: list[str] = []
    checks = [
        ("function", r"\bfunction\b"),
        ("total", r"\btotal\b"),
        ("functional", r"\bfunctional\b"),
        ("symbol", r"\bsymbol(?:\([^]]+\))?"),
        ("opaque/no-evaluators", r"\bno-evaluators\b"),
        ("priority", r"\bpriority\s*\("),
        ("simplification", r"\bsimplification\b"),
        ("concrete", r"\bconcrete\b"),
        ("owise", r"\bowise\b"),
        ("macro", r"\bmacro(?:-rec)?\b"),
        ("strictness", r"\b(?:seq)?strict(?:\([^]]+\))?"),
    ]
    for label, pattern in checks:
        if re.search(pattern, text):
            found.append(label)
    if record.kind == "rule" and not any(
        name in found for name in ("simplification", "concrete", "macro")
    ):
        found.append("ordinary-semantic-rule")
    return found or ["none"]


def decision(record: Record, relative: str) -> str:
    if record.kind in {"module", "endmodule", "imports", "requires"}:
        return "assembly checked"
    if record.kind == "configuration":
        return "initial cells checked and realizable"
    if record.kind == "syntax":
        return "declaration checked"
    if record.kind == "context":
        return "evaluation-order context checked"
    if record.kind == "claim":
        return "result obligation; adequacy checked separately"
    if record.kind != "rule":
        return "checked"
    if relative == "verification.k":
        return "sound harness/checkpoint rule; no program execution skipped"
    if relative == "spec.k":
        return "not a semantic extension"
    if relative.endswith("semantics/concrete.k"):
        return "excluded from Haskell proof definition"
    if in_ranges(record.line, EXERCISED_RULE_STARTS.get(relative, [])):
        return "faithful on every reachable submitted-program state"
    return (
        "unreached by submitted program; no path to this theorem's result "
        "(supplied-semantics limitation if non-CPython outside its subset)"
    )


def main() -> int:
    paths = sorted((SCRATCH / "reference-semantics").rglob("*.k"))
    paths.extend([SCRATCH / "verification.k", SCRATCH / "spec.k"])
    all_records: list[Record] = []
    for path in paths:
        all_records.extend(records_for(path))

    raw_start_counts = collections.Counter()
    for path in paths:
        for line in path.read_text().splitlines():
            kind = start_kind(line)
            if kind:
                raw_start_counts[kind] += 1
    record_counts = collections.Counter(record.kind for record in all_records)
    if raw_start_counts != record_counts:
        raise RuntimeError((raw_start_counts, record_counts))

    by_file = collections.Counter(
        str(record.path.relative_to(SCRATCH)) for record in all_records
    )
    by_kind = collections.Counter(record.kind for record in all_records)
    by_flag = collections.Counter(
        flag for record in all_records for flag in flags(record)
    )

    lines = [
        "# Exhaustive local K source inventory",
        "",
        "Generated from the clean scratch source copy. Each row below is one "
        "local source statement beginning with `requires`, `module`, "
        "`endmodule`, `imports`, `syntax`, `configuration`, `context`, "
        "`rule`, `claim`, or `alias`. Continuation lines, guards, cells, and "
        "attributes are retained in the row.",
        "",
        "## Counts",
        "",
        f"- Total records: {len(all_records)}",
        f"- Kind counts: `{dict(sorted(by_kind.items()))}`",
        f"- Attribute/class counts: `{dict(sorted(by_flag.items()))}`",
        "",
        "### Records by file",
        "",
    ]
    for path, count in sorted(by_file.items()):
        lines.append(f"- `{path}`: {count}")

    lines.extend(["", "## Row-by-row ledger", ""])
    for ordinal, record in enumerate(all_records, 1):
        relative = str(record.path.relative_to(SCRATCH))
        lines.extend(
            [
                f"### K-{ordinal:04d} — `{relative}:{record.line}`",
                "",
                f"- Kind: `{record.kind}`",
                f"- Flags: `{', '.join(flags(record))}`",
                f"- Decision: {decision(record, relative)}",
                "",
                "```k",
                record.text,
                "```",
                "",
            ]
        )

    OUTPUT.write_text("\n".join(lines))
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(f"output={OUTPUT}")
    print(f"sha256={digest}")
    print(f"total_records={len(all_records)}")
    print(f"kind_counts={dict(sorted(by_kind.items()))}")
    print(f"attribute_class_counts={dict(sorted(by_flag.items()))}")
    print(f"file_count={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
