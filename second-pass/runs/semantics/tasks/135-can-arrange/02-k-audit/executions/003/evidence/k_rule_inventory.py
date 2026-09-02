#!/usr/bin/env python3
"""Enumerate every local K declaration/rule in the supplied and proof sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/135-can-arrange")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(syntax|configuration|rule|claim|context|alias|endmodule)\b"
)


def records(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for number, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            starts.append((number, match.group(1)))
    result: list[tuple[int, str, str]] = []
    for index, (number, kind) in enumerate(starts):
        end = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
        text = "\n".join(lines[number - 1 : end]).strip()
        if kind != "endmodule":
            result.append((number, kind, text))
    return result


def tags(kind: str, text: str, provenance: str) -> list[str]:
    result = [provenance]
    code_only = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
    lowered = code_only.lower()
    if kind == "syntax":
        if "function" in lowered:
            result.append("function-declaration")
        else:
            result.append("syntax-declaration")
        for attribute in (
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", lowered):
                result.append(attribute)
    elif kind == "rule":
        result.append("semantic-rule" if "<k>" in text else "equational-rule")
        for attribute in ("priority", "simplification", "owise", "concrete"):
            if re.search(rf"\b{attribute}\b", lowered):
                result.append(attribute)
    elif kind == "claim":
        result.append("reachability-claim")
    elif kind == "context":
        result.append("evaluation-context")
    elif kind == "configuration":
        result.append("configuration")
    return result


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).replace("\t", " ").strip()


def main() -> int:
    counts: Counter[str] = Counter()
    total = 0
    for path in FILES:
        provenance = (
            "candidate-local"
            if path.name in {"verification.k", "spec.k"}
            else "supplied-baseline"
        )
        rel = path.relative_to(ROOT)
        for line, kind, text in records(path):
            record_tags = tags(kind, text, provenance)
            counts[kind] += 1
            for tag in record_tags:
                counts[f"tag:{tag}"] += 1
            total += 1
            print(
                f"{rel}:{line}\t{kind}\t{','.join(record_tags)}\t{one_line(text)}"
            )
    print(f"TOTAL_RECORDS\t{total}")
    for key, count in sorted(counts.items()):
        print(f"COUNT\t{key}\t{count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
