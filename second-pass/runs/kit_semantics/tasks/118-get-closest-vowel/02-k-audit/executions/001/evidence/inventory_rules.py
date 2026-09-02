#!/usr/bin/env python3
"""Inventory every top-level K declaration in supplied and proof-local sources."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
LOCAL_NAMES = (
    "foundation.k",
    "helper-verification.k",
    "verification.k",
    "connection-spec.k",
    "loop-connection-spec.k",
    "spec.k",
)
START = re.compile(
    r"^  (syntax|rule|claim|context|configuration|alias)\b"
)
ATTR = re.compile(r"\[([^\]]+)\]")


def declarations(path: Path):
    lines = path.read_text().splitlines()
    starts: list[int] = []
    for index, line in enumerate(lines):
        if START.match(line):
            starts.append(index)
    for number, start in enumerate(starts):
        stop = starts[number + 1] if number + 1 < len(starts) else len(lines)
        for index in range(start + 1, stop):
            if lines[index].startswith("endmodule"):
                stop = index
                break
        block = "\n".join(lines[start:stop]).rstrip()
        kind = START.match(lines[start]).group(1)  # type: ignore[union-attr]
        attributes = sorted(
            {
                token.strip()
                for attr in ATTR.findall(block)
                for token in attr.split(",")
            }
        )
        normalized = " ".join(part.strip() for part in block.splitlines())
        yield start + 1, kind, attributes, normalized


def classify(kind: str, attributes: list[str]) -> str:
    tags: list[str] = []
    if kind == "syntax":
        tags.append("declaration")
        if "function" in attributes:
            tags.append("function")
        if "total" in attributes:
            tags.append("total")
        if any(attribute.startswith("symbol") for attribute in attributes):
            tags.append("symbol")
        if "no-evaluators" in attributes:
            tags.append("opaque/no-evaluators")
        if "macro" in attributes:
            tags.append("macro")
    elif kind == "rule":
        tags.append("semantic-rule")
        if "simplification" in attributes:
            tags.append("simplification")
        if any(attribute.startswith("priority") for attribute in attributes):
            tags.append("priority")
        if "concrete" in attributes:
            tags.append("concrete")
        if "owise" in attributes:
            tags.append("owise")
    elif kind == "claim":
        tags.append("reachability-claim")
    else:
        tags.append(kind)
    return ",".join(tags)


def emit_group(label: str, paths: list[Path]) -> Counter[str]:
    counts: Counter[str] = Counter()
    print(f"GROUP {label}")
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        for line, kind, attributes, normalized in declarations(path):
            counts[kind] += 1
            classification = classify(kind, attributes)
            digest = hashlib.sha256(normalized.encode()).hexdigest()[:16]
            print(
                f"{relative}:{line} kind={kind} class={classification} "
                f"attrs={attributes!r} sha256_16={digest} text={normalized}"
            )
    print(f"COUNTS {label} {dict(sorted(counts.items()))}")
    return counts


def main() -> None:
    supplied = sorted((ROOT / "reference-semantics").rglob("*.k"))
    local = [ROOT / name for name in LOCAL_NAMES]
    supplied_counts = emit_group("SUPPLIED_SEMANTICS", supplied)
    local_counts = emit_group("PROOF_LOCAL", local)
    print(
        f"TOTAL supplied={sum(supplied_counts.values())} "
        f"proof_local={sum(local_counts.values())}"
    )


if __name__ == "__main__":
    main()
