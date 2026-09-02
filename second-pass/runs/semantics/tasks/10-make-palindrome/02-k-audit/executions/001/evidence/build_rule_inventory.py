#!/usr/bin/env python3
"""Create a complete source-indexed inventory of K declarations and rules."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


CANDIDATE = Path("/candidate")
OUTPUT = Path("/audit-output/evidence/rule-inventory.txt")
START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")


def classify(kind: str, text: str) -> str:
    tags: list[str] = [kind]
    if kind == "syntax":
        for attr in (
            "function",
            "functional",
            "total",
            "macro",
            "macro-rec",
            "symbol",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", text):
                tags.append(attr)
    if kind == "rule":
        for attr in ("priority", "simplification", "owise", "anywhere", "concrete"):
            if re.search(rf"\b{re.escape(attr)}\b", text):
                tags.append(attr)
    return "+".join(tags)


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for offset, start in enumerate(starts):
        next_start = starts[offset + 1] if offset + 1 < len(starts) else len(lines)
        stop = next_start
        while stop > start + 1 and not lines[stop - 1].strip():
            stop -= 1
        match = START.match(lines[start])
        assert match is not None
        yield start + 1, match.group(1), "\n".join(lines[start:stop]).rstrip()


def main() -> int:
    paths = [
        CANDIDATE / "reference-semantics" / "semantics.k",
        *sorted((CANDIDATE / "reference-semantics" / "semantics").glob("*.k")),
        CANDIDATE / "verification.k",
    ]
    count_by_class: Counter[str] = Counter()
    count_by_file: Counter[str] = Counter()
    inventory: list[str] = []

    for path in paths:
        relative = path.relative_to(CANDIDATE)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        inventory.append(f"\n=== FILE {relative} sha256={digest} ===")
        for line, kind, text in blocks(path):
            category = classify(kind, text)
            count_by_class[category] += 1
            count_by_file[str(relative)] += 1
            flattened = " ".join(part.strip() for part in text.splitlines())
            inventory.append(
                f"{relative}:{line} [{category}] {flattened}"
            )

    header = [
        "K SOURCE INVENTORY",
        "Scope: candidate supplied-semantics tree plus candidate verification.k.",
        "Each configuration, syntax declaration, context, rule, and claim is listed once.",
        "",
        "COUNTS BY CLASS",
        *(
            f"{category}: {count}"
            for category, count in sorted(count_by_class.items())
        ),
        "",
        "COUNTS BY FILE",
        *(f"{path}: {count}" for path, count in sorted(count_by_file.items())),
        "",
        f"TOTAL INVENTORIED ITEMS: {sum(count_by_class.values())}",
    ]
    OUTPUT.write_text("\n".join(header + inventory) + "\n", encoding="utf-8")

    print(f"output={OUTPUT}")
    print(f"file_count={len(paths)}")
    print(f"total_items={sum(count_by_class.values())}")
    print("counts_by_class=")
    for category, count in sorted(count_by_class.items()):
        print(f"  {category}: {count}")
    print(f"sha256={hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
