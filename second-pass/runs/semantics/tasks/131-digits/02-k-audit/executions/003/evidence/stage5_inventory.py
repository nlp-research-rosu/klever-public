#!/usr/bin/env python3
"""Exhaustive source-level inventory of K declarations and rules."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


SEMANTICS_ROOT = Path("/reference/reference-semantics")
EXTRA_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
START = re.compile(
    r"^\s*(syntax|rule|claim|context|configuration|alias)\b"
)
ATTR = re.compile(
    r"\b(function|functional|total|simplification|priority|opaque|symbol|"
    r"no-evaluators|macro|owise|concrete|anywhere)\b"
)


def inventory_file(path: Path) -> Counter[str]:
    raw_lines = path.read_text().splitlines()
    filtered = [
        (original_index, line)
        for original_index, line in enumerate(raw_lines)
        if not line.lstrip().startswith("//")
    ]
    lines = [line for _, line in filtered]
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))

    counts: Counter[str] = Counter()
    print(f"FILE {path}")
    for item_index, (start, kind) in enumerate(starts):
        stop = starts[item_index + 1][0] if item_index + 1 < len(starts) else len(lines)
        block_lines = lines[start:stop]
        while block_lines and block_lines[-1].strip() in {
            "",
            "endmodule",
        }:
            block_lines.pop()
        text = re.sub(r"\s+", " ", " ".join(block_lines)).strip()
        source_line = filtered[start][0] + 1
        attributes = sorted(set(ATTR.findall(text)))
        counts[kind] += 1
        for attribute in attributes:
            counts[f"attr:{attribute}"] += 1
        print(
            f"  ITEM kind={kind} line={source_line} "
            f"attrs={','.join(attributes) or '-'} :: {text}"
        )
    print(
        "  COUNTS "
        + " ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    )
    return counts


def main() -> None:
    files = [SEMANTICS_ROOT / "semantics.k"]
    files.extend(sorted((SEMANTICS_ROOT / "semantics").glob("*.k")))
    files.extend(EXTRA_FILES)
    total: Counter[str] = Counter()
    for path in files:
        total.update(inventory_file(path))
    print("GRAND_COUNTS " + " ".join(f"{k}={v}" for k, v in sorted(total.items())))

    trusted_text = "\n".join(path.read_text() for path in files[:-2])
    proof_text = "\n".join(path.read_text() for path in EXTRA_FILES)
    for needle in ["oddDigitProduct", "oddDigitStep", "digits", "131"]:
        print(
            f"TASK_TOKEN {needle!r} "
            f"trusted_semantics_occurrences={trusted_text.count(needle)} "
            f"proof_occurrences={proof_text.count(needle)}"
        )
    print("STAGE5_INVENTORY_OK")


if __name__ == "__main__":
    main()
