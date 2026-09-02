#!/usr/bin/env python3
"""Enumerate every K declaration/rule-like sentence in the audited sources."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


START = re.compile(
    r"^ {0,2}(requires|module|endmodule|imports|configuration|syntax|rule|claim|"
    r"context|context alias|alias)\b"
)


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def entries(path: Path) -> list[dict[str, object]]:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    clean_lines = strip_comments(path.read_text(encoding="utf-8")).splitlines()
    starts = [
        index
        for index, line in enumerate(clean_lines)
        if START.match(line)
    ]
    result: list[dict[str, object]] = []
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(clean_lines)
        kind = START.match(clean_lines[start]).group(1)  # type: ignore[union-attr]
        block = " ".join(
            line.strip()
            for line in clean_lines[start:stop]
            if line.strip()
        )
        raw_block = "\n".join(raw_lines[start:stop])
        candidate_attributes = re.findall(r"\[([^\]]+)\]", raw_block, flags=re.DOTALL)
        attributes = [
            value
            for value in candidate_attributes
            if re.search(
                r"\b(function|functional|total|owise|concrete|simplification|"
                r"macro|macro-rec|priority|strict|seqstrict|symbol|no-evaluators)\b",
                value,
            )
        ]
        result.append(
            {
                "file": str(path),
                "line": start + 1,
                "kind": kind,
                "attributes": [" ".join(value.split()) for value in attributes],
                "text": block,
            }
        )
    return result


def main() -> int:
    paths = [Path(argument) for argument in sys.argv[1:]]
    inventory = [entry for path in paths for entry in entries(path)]
    counts: dict[str, int] = {}
    for entry in inventory:
        key = str(entry["kind"])
        counts[key] = counts.get(key, 0) + 1
        print(json.dumps(entry, sort_keys=True))
    print(json.dumps({"counts": counts, "files": len(paths), "entries": len(inventory)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
