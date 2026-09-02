#!/usr/bin/env python3
"""Line-addressed inventory of every K declaration and rule in the audit sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/25-factorize")
FILES = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|context(?:\s+alias)?|rule|claim)\b"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "macro",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
    "priority",
    "owise",
    "concrete",
    "simplification",
)


def without_line_comment(line: str) -> str:
    # These sources use // comments; no URL or quoted // occurs in declarations.
    return line.split("//", 1)[0].rstrip()


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        clean = without_line_comment(line)
        match = START.match(clean)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = "\n".join(lines[start:stop]).rstrip()
        yield start + 1, stop, kind, body


def classify(kind: str, body: str) -> str:
    tags: list[str] = []
    if kind == "rule":
        tags.append("operational" if "<k>" in body else "equational")
    for attr in ATTRS:
        if re.search(rf"\b{re.escape(attr)}\b", body):
            tags.append(attr)
    return ",".join(tags) if tags else "-"


def main() -> int:
    global_kinds: collections.Counter[str] = collections.Counter()
    global_attrs: collections.Counter[str] = collections.Counter()
    print(f"file_count={len(FILES)}")
    for path in FILES:
        rel = path.relative_to(ROOT)
        records = list(blocks(path))
        kinds = collections.Counter(kind for _, _, kind, _ in records)
        attrs: collections.Counter[str] = collections.Counter()
        for _, _, _, body in records:
            for attr in ATTRS:
                if re.search(rf"\b{re.escape(attr)}\b", body):
                    attrs[attr] += 1
        global_kinds.update(kinds)
        global_attrs.update(attrs)
        print(f"\n===== FILE {rel} lines={sum(1 for _ in path.open(encoding='utf-8'))}")
        print(f"COUNTS kinds={dict(kinds)} attributed_blocks={dict(attrs)}")
        for start, stop, kind, body in records:
            print(f"\n--- {rel}:{start}-{stop} kind={kind} class={classify(kind, body)}")
            print(body)
    print(f"\nGLOBAL kind_counts={dict(global_kinds)}")
    print(f"GLOBAL attributed_block_counts={dict(global_attrs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
