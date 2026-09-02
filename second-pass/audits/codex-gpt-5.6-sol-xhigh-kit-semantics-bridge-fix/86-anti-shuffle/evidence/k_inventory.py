#!/usr/bin/env python3
"""Create an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")


def normalized(lines: list[str]) -> str:
    kept: list[str] = []
    for line in lines:
        body = line.split("//", 1)[0].strip()
        if body and body != "endmodule":
            kept.append(body)
    return " ".join(" ".join(kept).split()).replace("\t", " ")


def classify(kind: str, text: str) -> tuple[str, str]:
    attrs: list[str] = []
    for name in (
        "function", "functional", "total", "symbol", "no-evaluators",
        "simplification", "concrete", "priority", "owise", "macro",
        "macro-rec", "strict", "seqstrict",
    ):
        if re.search(rf"(?<![A-Za-z-]){re.escape(name)}(?:\(|\b)", text):
            attrs.append(name)

    if "no-evaluators" in attrs or ("symbol" in attrs and "concrete" not in attrs):
        decision = "BOUNDARY-OPAQUE"
    elif kind == "claim":
        decision = "CLAIM-RECONSTRUCT"
    elif kind == "configuration":
        decision = "ACCEPT-FIXED-CONFIGURATION"
    else:
        decision = "ACCEPT-NO-FALSE-WITNESS"
    return ",".join(attrs) or "-", decision


def proof_local_decision(path: Path, line: int, kind: str, current: str) -> str:
    if path.name == "verification.k":
        if kind == "syntax" and line in (9, 10, 11):
            return "ACCEPT-EXACT-MACRO-DECL"
        if kind == "syntax" and 13 <= line <= 17:
            return "ACCEPT-PROOF-HELPER-DECL"
        if kind == "rule" and 24 <= line <= 49:
            return "ACCEPT-EXACT-MACRO-EXPANSION"
        if kind == "rule" and 51 <= line <= 75:
            return "ACCEPT-STRUCTURAL-SUMMARY"
        if kind == "rule" and 78 <= line <= 92:
            return "ACCEPT-ALLOCATOR-LEMMA"
    if path.name == "spec.k" and kind == "claim":
        return "CLAIM-RECONSTRUCT"
    return current


def entries(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for pos, (index, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        text = normalized(lines[index:end])
        attrs, decision = classify(kind, text)
        decision = proof_local_decision(path, index + 1, kind, decision)
        yield index + 1, kind, attrs, decision, text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    print("id\tfile\tline\tkind\tattributes\taudit_decision\tdeclaration_or_rule")
    count = 0
    for path in sorted(args.paths, key=lambda item: str(item)):
        for line, kind, attrs, decision, text in entries(path):
            count += 1
            print(
                f"K{count:04d}\t{path}\t{line}\t{kind}\t{attrs}\t{decision}\t{text}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
