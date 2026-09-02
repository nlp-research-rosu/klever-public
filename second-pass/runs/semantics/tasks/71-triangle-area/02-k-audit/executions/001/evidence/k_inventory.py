#!/usr/bin/env python3
"""Emit an exhaustive, line-numbered declaration/rule inventory for K sources."""

from __future__ import annotations

import re
import sys
from pathlib import Path


START = re.compile(
    r"^(?:requires|module|endmodule)\b"
    r"|^  (?:imports|configuration|syntax|context|rule|claim)\b"
)

ATTR_MARKERS = (
    "function",
    "functional",
    "total",
    "symbol(",
    "no-evaluators",
    "priority(",
    "owise",
    "concrete",
    "simplification",
)


def blocks(path: Path) -> list[tuple[int, int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    out: list[tuple[int, int, str]] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:end]).rstrip()
        out.append((start + 1, end, text))
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: k_inventory.py FILE_OR_DIRECTORY [...]", file=sys.stderr)
        return 64

    paths: list[Path] = []
    for arg in sys.argv[1:]:
        path = Path(arg)
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.k")))
        else:
            paths.append(path)

    total = 0
    per_kind: dict[str, int] = {}
    marker_counts = {marker: 0 for marker in ATTR_MARKERS}
    for path in sorted(set(paths)):
        print(f"===== {path} =====")
        file_blocks = blocks(path)
        file_kinds: dict[str, int] = {}
        file_markers = {marker: 0 for marker in ATTR_MARKERS}
        for start, end, text in file_blocks:
            first = text.lstrip().split(None, 1)[0]
            per_kind[first] = per_kind.get(first, 0) + 1
            file_kinds[first] = file_kinds.get(first, 0) + 1
            present = [marker for marker in ATTR_MARKERS if marker in text]
            for marker in present:
                marker_counts[marker] += 1
                file_markers[marker] += 1
            total += 1
            metadata = ",".join(present) if present else "none"
            print(f"--- lines {start}-{end} kind={first} markers={metadata} ---")
            print(text)
        print(
            "FILE_COUNTS: "
            + " ".join(f"{kind}={file_kinds[kind]}" for kind in sorted(file_kinds))
        )
        print(
            "FILE_MARKERS: "
            + " ".join(
                f"{marker}={file_markers[marker]}" for marker in ATTR_MARKERS
            )
        )
        print()
    print(f"TOTAL_BLOCKS: {total}")
    print("COUNTS: " + " ".join(f"{kind}={per_kind[kind]}" for kind in sorted(per_kind)))
    print(
        "MARKER_COUNTS: "
        + " ".join(f"{marker}={marker_counts[marker]}" for marker in ATTR_MARKERS)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
