#!/usr/bin/env python3
"""Produce a source-located inventory of every local K declaration."""

from __future__ import annotations

import re
from pathlib import Path


SEMANTICS_ROOT = Path(
    "/tmp/audit-work/reconstruction/reference-semantics"
)
FILES = sorted(SEMANTICS_ROOT.rglob("*.k")) + [
    Path("/tmp/audit-work/reconstruction/verification.k"),
    Path("/tmp/audit-work/reconstruction/spec.k"),
]
START = re.compile(
    r"^\s*(configuration|syntax|rule|context(?:\s+alias)?|claim)\b"
)
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|rule|context(?:\s+alias)?|claim|"
    r"module|endmodule|imports|requires)\b"
)


def classification(path: Path, kind: str, declaration: str) -> str:
    tags: list[str] = []
    if "[function" in declaration or ", function" in declaration:
        tags.append("function")
    if "total" in declaration:
        tags.append("total")
    if "functional" in declaration:
        tags.append("functional")
    if "no-evaluators" in declaration or "symbol(" in declaration:
        tags.append("opaque-or-external-symbol")
    if "simplification" in declaration:
        tags.append("simplification")
    if "priority(" in declaration:
        tags.append("priority")
    if "owise" in declaration:
        tags.append("owise")
    if "concrete" in declaration:
        tags.append("concrete")
    if path.name == "verification.k":
        disposition = "proof-local: individually reviewed in REVIEW.md"
    elif path.name == "spec.k":
        disposition = "reachability claim: adequacy reviewed in REVIEW.md"
    else:
        disposition = "fixed supplied semantics"
    return ",".join(tags) if tags else kind, disposition


def declarations(path: Path):
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        start = index
        kind = match.group(1)
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            index += 1
        block = " ".join(
            part.strip()
            for part in lines[start:index]
            if part.strip() and not part.lstrip().startswith("//")
        )
        yield start + 1, kind, block


def main() -> None:
    print("source\tline\tkind\tattributes\tdisposition\tdeclaration")
    count = 0
    for path in FILES:
        relative = (
            path.relative_to("/tmp/audit-work/reconstruction").as_posix()
        )
        for line, kind, declaration in declarations(path):
            attributes, disposition = classification(path, kind, declaration)
            safe = declaration.replace("\t", " ")
            print(
                f"{relative}\t{line}\t{kind}\t{attributes}\t"
                f"{disposition}\t{safe}"
            )
            count += 1
    print(f"# declaration_count={count}")


if __name__ == "__main__":
    main()
