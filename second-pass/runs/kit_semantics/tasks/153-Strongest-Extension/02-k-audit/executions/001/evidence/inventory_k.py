#!/usr/bin/env python3
"""Produce a line-addressed inventory of K declarations and rules."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


REFERENCE_ROOT = Path("/reference/reference-semantics")
CANDIDATE_FILES = [
    Path("/candidate/verification.k"),
    Path("/candidate/connection-spec.k"),
    Path("/candidate/outer-connection-spec.k"),
    Path("/candidate/spec.k"),
]
START = re.compile(
    r"^(?:(requires)\b|\s*(module|endmodule|imports|configuration|"
    r"syntax|rule|claim|context|alias)\b)"
)


def normalized(lines: list[str]) -> str:
    return " ".join(" ".join(lines).split())


def flags(text: str) -> str:
    known = [
        "function",
        "total",
        "functional",
        "no-evaluators",
        "macro",
        "simplification",
        "concrete",
        "symbolic",
        "preserves-definedness",
        "priority",
        "owise",
        "anywhere",
        "heat",
        "cool",
        "strict",
        "seqstrict",
        "assoc",
        "comm",
        "unit",
        "constructor",
        "cell",
        "maincell",
        "token",
    ]
    attributes = " ".join(re.findall(r"\[[^\]]*\]", text))
    return ",".join(flag for flag in known if flag in attributes)


def declarations(path: Path):
    lines = path.read_text().splitlines()
    starts = [
        (index, START.match(line))
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    for position, (index, match) in enumerate(starts):
        assert match is not None
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        statement_lines = lines[index:end]
        text = normalized(statement_lines)
        yield index + 1, match.group(1) or match.group(2), text


def main() -> int:
    files = sorted(REFERENCE_ROOT.rglob("*.k")) + CANDIDATE_FILES
    print("scope\tfile\tline\tkind\tflags\tsha256\tstatement")
    counts: dict[tuple[str, str], int] = {}
    for path in files:
        scope = "supplied" if path.is_relative_to(REFERENCE_ROOT) else "candidate"
        display = path.as_posix()
        for line, kind, text in declarations(path):
            digest = hashlib.sha256(text.encode()).hexdigest()
            print(
                f"{scope}\t{display}\t{line}\t{kind}\t{flags(text)}\t"
                f"{digest}\t{text}"
            )
            counts[(scope, kind)] = counts.get((scope, kind), 0) + 1
    print("# SUMMARY")
    for (scope, kind), count in sorted(counts.items()):
        print(f"# {scope}\t{kind}\t{count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
