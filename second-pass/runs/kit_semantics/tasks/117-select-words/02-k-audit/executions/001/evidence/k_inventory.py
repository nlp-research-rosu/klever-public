#!/usr/bin/env python3
"""Inventory top-level K declarations without trusting compiled definitions."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


START = re.compile(
    r'^\s*(requires(?=\s+"[^"]+"\s*$)|module|imports|'
    r"syntax(?:\s+priority|\s+associativity)?|configuration|rule|context|"
    r"alias|claim)\b"
)
ATTR = re.compile(r"\[([^\]]+)\]")
KNOWN_ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "macro",
    "alias",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
)


def normalize(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines)
    text = re.sub(r"\s+", " ", text)
    return text.replace("\t", " ")


def scan(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))

    records: list[dict[str, object]] = []
    for pos, (start, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        while end > start and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        block = lines[start:end]
        text = normalize(block)
        attrs = sorted(
            {
                match.group(1).strip()
                for match in ATTR.finditer(text)
                if any(name in match.group(1) for name in KNOWN_ATTRIBUTES)
            }
        )
        source_class = (
            "proof-local"
            if path.name in {"verification.k", "spec.k"}
            else "trusted-supplied"
        )
        if kind.startswith("syntax"):
            semantic_class = "syntax"
        elif kind == "rule":
            if "<k>" in text or "<heap>" in text or "<scopes>" in text:
                semantic_class = "operational-rule"
            else:
                semantic_class = "equational-rule"
        elif kind == "claim":
            semantic_class = "reachability-claim"
        elif kind == "context":
            semantic_class = "evaluation-context"
        else:
            semantic_class = kind
        records.append(
            {
                "file": str(path),
                "start": start + 1,
                "end": end,
                "kind": kind,
                "source_class": source_class,
                "semantic_class": semantic_class,
                "attrs": ",".join(attrs),
                "text": text,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()

    records: list[dict[str, object]] = []
    for path in args.files:
        records.extend(scan(path))

    print(
        "id\tfile\tlines\tkind\tsource_class\tsemantic_class\tattributes\tdeclaration"
    )
    for index, record in enumerate(records, 1):
        print(
            "\t".join(
                [
                    f"K{index:04d}",
                    str(record["file"]),
                    f'{record["start"]}-{record["end"]}',
                    str(record["kind"]),
                    str(record["source_class"]),
                    str(record["semantic_class"]),
                    str(record["attrs"]),
                    str(record["text"]),
                ]
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
