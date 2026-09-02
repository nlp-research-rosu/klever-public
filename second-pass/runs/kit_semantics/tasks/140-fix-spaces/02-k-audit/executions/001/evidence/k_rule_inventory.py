#!/usr/bin/env python3
"""Create a complete lexical inventory of supplied and proof-local K declarations."""

from __future__ import annotations

import collections
import re
from pathlib import Path


SEMANTICS_ROOT = Path("/tmp/audit-work/candidate-src/reference-semantics")
LOCAL_ROOT = Path("/tmp/audit-work/candidate-src")
OUTPUT = Path("/audit-output/evidence/04-rule-inventory.tsv")

DECLARATION = re.compile(
    r'^\s*(requires(?=\s+")|module|endmodule|imports|syntax|configuration|context|rule|claim|alias)\b'
)


def compact(lines: list[str]) -> str:
    without_comments = []
    for line in lines:
        code = line.split("//", 1)[0].strip()
        if code:
            without_comments.append(code)
    return " ".join(" ".join(without_comments).split())


def category(kind: str, body: str) -> str:
    if kind == "syntax":
        tags = []
        for token in (
            "function",
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "macro-rec",
            "macro",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(token)}\b", body):
                tags.append(token)
        return "syntax" + (":" + ",".join(tags) if tags else "")
    if kind == "rule":
        tags = []
        for token in ("simplification", "priority", "concrete", "owise"):
            if re.search(rf"\b{re.escape(token)}\b", body):
                tags.append(token)
        return "rule" + (":" + ",".join(tags) if tags else ":ordinary")
    return kind


def extract_declarations(path: Path) -> list[tuple[int, str, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = DECLARATION.match(line)
        if match:
            starts.append((index, match.group(1)))
    result = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = compact(lines[start:end])
        result.append((start + 1, kind, category(kind, body), body))
    return result


def main() -> int:
    files = sorted(SEMANTICS_ROOT.rglob("*.k"))
    files.extend([LOCAL_ROOT / "verification.k", LOCAL_ROOT / "spec.k"])
    rows: list[tuple[str, int, str, str, str]] = []
    counts: collections.Counter[str] = collections.Counter()
    for path in files:
        if path.is_relative_to(SEMANTICS_ROOT):
            display = "reference-semantics/" + path.relative_to(SEMANTICS_ROOT).as_posix()
        else:
            display = path.name
        for line, kind, classification, body in extract_declarations(path):
            rows.append((display, line, kind, classification, body))
            counts[classification] += 1

    header = "file\tline\tdeclaration\tclassification\ttext"
    with OUTPUT.open("w", encoding="utf-8") as stream:
        stream.write(header + "\n")
        for row in rows:
            stream.write("\t".join(str(item).replace("\t", " ") for item in row) + "\n")

    print(f"files_scanned={len(files)}")
    print(f"declarations={len(rows)}")
    for key, value in sorted(counts.items()):
        print(f"{key}={value}")

    print("opaque/no-evaluator declarations:")
    for display, line, kind, classification, body in rows:
        if kind == "syntax" and (
            "no-evaluators" in body
            or ("symbol(" in body and "[function" in body and "[concrete]" not in body)
        ):
            print(f"  {display}:{line}: {body}")

    print("priority rules:")
    for display, line, kind, classification, body in rows:
        if kind == "rule" and "priority" in classification:
            print(f"  {display}:{line}: {body}")

    print("simplification rules:")
    for display, line, kind, classification, body in rows:
        if kind == "rule" and "simplification" in classification:
            print(f"  {display}:{line}: {body}")

    print("claims:")
    for display, line, kind, classification, body in rows:
        if kind == "claim":
            print(f"  {display}:{line}: {body}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
