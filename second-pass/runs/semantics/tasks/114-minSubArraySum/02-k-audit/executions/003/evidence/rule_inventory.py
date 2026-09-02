#!/usr/bin/env python3
"""Exhaustive source-level declaration/rule inventory for this audit."""

from __future__ import annotations

import collections
import re
from pathlib import Path

SEMANTICS = Path("/reference/reference-semantics")
CANDIDATE_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
FILES = sorted(SEMANTICS.rglob("*.k"), key=lambda p: p.as_posix()) + CANDIDATE_FILES

START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
STOP = re.compile(r"^\s*(module|endmodule)\b")


def statements(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [(index, START.match(line).group(1)) for index, line in enumerate(lines) if START.match(line)]
    result: list[tuple[int, str, str]] = []
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        for cursor in range(index + 1, end):
            if STOP.match(lines[cursor]):
                end = cursor
                break
        segment = lines[index:end]
        while segment and (not segment[-1].strip() or segment[-1].lstrip().startswith("//")):
            segment.pop()
        normalized = " ".join(part.strip() for part in segment if part.strip() and not part.lstrip().startswith("//"))
        result.append((index + 1, kind, normalized))
    return result


def classify(kind: str, text: str) -> str:
    classes: list[str] = [kind]
    if kind == "syntax":
        if "[function" in text or ", function" in text:
            classes.append("function")
        if "functional" in text:
            classes.append("functional")
        if "total" in text:
            classes.append("total")
        if "no-evaluators" in text:
            classes.append("opaque/no-evaluators")
        if "symbol(" in text:
            classes.append("symbol")
        if "macro-rec" in text:
            classes.append("macro-rec")
        elif "macro" in text:
            classes.append("macro")
        if not any(label in classes for label in ("function", "macro", "macro-rec")):
            classes.append("constructor/declaration")
    elif kind == "rule":
        classes.append("operational" if "<k>" in text else "equational")
        for token, label in [
            ("priority(", "priority"),
            ("simplification", "simplification"),
            ("[owise]", "owise"),
            ("[concrete]", "concrete-only"),
        ]:
            if token in text:
                classes.append(label)
    return ",".join(classes)


totals: collections.Counter[str] = collections.Counter()
print("# Exhaustive K source inventory")
print()
print("The supplied tree is inventoried once from the trusted mount because Stage 1")
print("established exact type/name/byte identity with candidate/reference-semantics.")
print("No other candidate helper K files exist.")
print()
for path in FILES:
    rows = statements(path)
    print(f"## {path}")
    print()
    local: collections.Counter[str] = collections.Counter()
    for line, kind, text in rows:
        classification = classify(kind, text)
        local[kind] += 1
        totals[kind] += 1
        for label in classification.split(","):
            totals[f"class:{label}"] += 1
        print(f"- L{line} [{classification}] `{text}`")
    print()
    print("Counts:", ", ".join(f"{name}={count}" for name, count in sorted(local.items())))
    print()

print("# Totals")
print()
for name, count in sorted(totals.items()):
    print(f"- {name}: {count}")
