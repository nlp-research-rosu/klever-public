#!/usr/bin/env python3
"""Create a complete source-level K declaration/rule inventory.

Each top-level K declaration is emitted with its entire source block and a
classification derived from its attributes. The trusted tree comparison is
recorded separately in stage1-integrity.log.
"""

from __future__ import annotations

import hashlib
import re
import sys
from collections import Counter
from pathlib import Path


START_RE = re.compile(
    r"^(?:(requires|module|endmodule)\b|  "
    r"(configuration|syntax|context|rule|claim|imports)\b)"
)


def classify(kind: str, body: str) -> str:
    labels = [kind]
    for attr in (
        "function",
        "functional",
        "total",
        "simplification",
        "priority",
        "owise",
        "macro",
        "strict",
        "seqstrict",
        "concrete",
        "symbol",
        "opaque",
        "no-evaluators",
    ):
        if re.search(rf"\b{re.escape(attr)}(?:\b|\()", body):
            labels.append(attr)
    if kind == "rule" and "priority" not in labels:
        labels.append("ordinary-or-equational")
    return ",".join(labels)


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START_RE.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for position, (start, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body_lines = lines[start:stop]
        while body_lines and (
            not body_lines[-1].strip() or body_lines[-1].lstrip().startswith("//")
        ):
            body_lines.pop()
        yield start + 1, kind, "\n".join(body_lines)


def main() -> int:
    root = Path(sys.argv[1])
    extra_files = [Path(item) for item in sys.argv[2:]]
    files = sorted(root.rglob("*.k")) + extra_files
    grand = Counter()
    attributes = Counter()
    print("COMPLETE K SOURCE INVENTORY")
    print(f"source_root={root}")
    print(f"file_count={len(files)}")
    for path in files:
        data = path.read_bytes()
        items = list(blocks(path))
        counts = Counter(kind for _, kind, _ in items)
        grand.update(counts)
        print()
        print(
            f"FILE {path} sha256={hashlib.sha256(data).hexdigest()} "
            f"bytes={len(data)} items={len(items)} counts={dict(sorted(counts.items()))}"
        )
        for line, kind, body in items:
            item_class = classify(kind, body)
            attributes.update(item_class.split(","))
            print(f"ITEM {path}:{line} class={item_class}")
            print(body)
            print("END_ITEM")
    print()
    print(f"GRAND_COUNTS={dict(sorted(grand.items()))}")
    print(f"ATTRIBUTE_COUNTS={dict(sorted(attributes.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
