#!/usr/bin/env python3
"""Create a source-indexed inventory of every K declaration and rule."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/rebuild")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^(?P<indent>\s*)"
    r"(?P<kind>"
    r"syntax(?:\s+(?:priority|priorities|associativity))?"
    r"|rule"
    r"|claim"
    r"|configuration"
    r"|context(?:\s+alias)?"
    r")\b"
)
BOUNDARY = re.compile(
    r"^\s*(?:module|endmodule|imports?|requires|syntax|rule|claim|"
    r"configuration|context)\b"
)


def classify(kind: str, text: str) -> list[str]:
    flags = []
    for flag in (
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "macro",
        "simplification",
        "anywhere",
        "owise",
    ):
        if re.search(rf"\b{re.escape(flag)}\b", text):
            flags.append(flag)
    priority = re.search(r"priority\s*\(\s*([0-9]+)\s*\)", text)
    if priority:
        flags.append(f"priority({priority.group(1)})")
    return flags


def blocks(path: Path) -> list[tuple[int, int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group("kind")))

    result = []
    for ordinal, (start, kind) in enumerate(starts):
        next_start = starts[ordinal + 1][0] if ordinal + 1 < len(starts) else len(lines)
        end = next_start
        # Stop before module-level boundaries/comments belonging to the next section.
        for index in range(start + 1, next_start):
            if BOUNDARY.match(lines[index]):
                end = index
                break
        while end > start + 1 and not lines[end - 1].strip():
            end -= 1
        text = "\n".join(lines[start:end])
        result.append((start + 1, end, kind, text))
    return result


def main() -> int:
    total_counts: Counter[str] = Counter()
    print("# Exhaustive K declaration/rule inventory")
    print()
    print(
        "Each item records the complete source block beginning at every "
        "`syntax`, `rule`, `claim`, `configuration`, or `context` declaration."
    )
    print()
    for path in FILES:
        relative = path.relative_to(ROOT).as_posix()
        file_blocks = blocks(path)
        counts = Counter(block[2] for block in file_blocks)
        total_counts.update(counts)
        print(f"## {relative}")
        print()
        print(
            f"Count: {len(file_blocks)}; "
            + ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        )
        print()
        for ordinal, (start, end, kind, text) in enumerate(file_blocks, 1):
            flags = classify(kind, text)
            flag_text = ", ".join(flags) if flags else "none"
            print(
                f"### {relative}:{start}-{end} [{ordinal}] "
                f"{kind}; attributes: {flag_text}"
            )
            print()
            print("```k")
            print(text)
            print("```")
            print()

    print("# Totals")
    print()
    print(", ".join(f"{key}={value}" for key, value in sorted(total_counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
