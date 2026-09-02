#!/usr/bin/env python3
"""Emit a complete line-addressed inventory of local K declarations and rules."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


START = re.compile(r"^\s*(configuration|syntax|context|rule|claim|alias)\b")
ATTRS = (
    "function",
    "functional",
    "total",
    "simplification",
    "macro",
    "macro-rec",
    "owise",
    "priority",
    "concrete",
    "symbol",
    "no-evaluators",
    "anywhere",
    "trusted",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for pos, start in enumerate(starts):
        stop = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        chunk = lines[start:stop]
        while chunk and (
            not chunk[-1].strip()
            or chunk[-1].lstrip().startswith("//")
            or chunk[-1].strip() in {"endmodule"}
        ):
            chunk.pop()
        normalized = " ".join(part.strip() for part in chunk if part.strip() and not part.lstrip().startswith("//"))
        kind = START.match(lines[start]).group(1)  # type: ignore[union-attr]
        attrs = [attr for attr in ATTRS if re.search(rf"\b{re.escape(attr)}\b", normalized)]
        role = ""
        if kind == "rule":
            if "[macro" in normalized:
                role = "macro"
            elif "<k>" in normalized or re.search(r"<[A-Za-z][^>]*>", normalized):
                role = "operational"
            elif "[simplification]" in normalized:
                role = "simplification"
            else:
                role = "equation"
        yield start + 1, kind, role, attrs, normalized


def main() -> int:
    roots = [
        Path("/reference/reference-semantics/semantics.k"),
        *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
    ]
    total = 0
    print("# Exhaustive K source inventory")
    print()
    print("Each declaration/rule/claim is identified by immutable source hash and line.")
    for path in roots:
        items = list(blocks(path))
        total += len(items)
        counts: dict[str, int] = {}
        for _, kind, _, _, _ in items:
            counts[kind] = counts.get(kind, 0) + 1
        print()
        print(f"## {path}")
        print()
        print(f"- SHA-256: `{sha256(path)}`")
        print(f"- Counts: `{counts}`")
        print()
        for line, kind, role, attrs, normalized in items:
            attr_text = ",".join(attrs) if attrs else "-"
            role_text = role or "-"
            print(
                f"- `{path}:{line}` kind=`{kind}` role=`{role_text}` "
                f"attributes=`{attr_text}` — {normalized}"
            )
    print()
    print(f"INVENTORY_ITEMS={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
