#!/usr/bin/env python3
"""Mechanical exhaustive declaration/rule inventory for the fixed theory."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


SOURCES = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

START = re.compile(
    r'^\s*(requires(?=\s+")|module|endmodule|imports|configuration|context|syntax|rule|claim)\b'
)


def statements(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            kind = "requires" if match.group(1).startswith("requires") else match.group(1)
            starts.append((index, kind))
    for offset, (index, kind) in enumerate(starts):
        stop = starts[offset + 1][0] if offset + 1 < len(starts) else len(lines)
        raw = lines[index:stop]
        while raw and (not raw[-1].strip() or raw[-1].lstrip().startswith("//")):
            raw.pop()
        text = "\n".join(raw).strip()
        yield index + 1, kind, text


def attrs(text: str) -> set[str]:
    found = set()
    for body in re.findall(r"\[([^\]]*)\]", text, flags=re.DOTALL):
        for item in body.split(","):
            item = item.strip()
            if item:
                found.add(item)
    return found


def syntax_class(text: str) -> str:
    attributes = attrs(text)
    classes = ["syntax"]
    for name in [
        "function",
        "total",
        "functional",
        "macro",
        "macro-rec",
        "concrete",
        "no-evaluators",
    ]:
        if name in attributes:
            classes.append(name)
    if any(item.startswith("symbol(") for item in attributes):
        classes.append("symbol")
    if "symbol" in classes and "no-evaluators" in classes:
        classes.append("opaque-in-proof")
    return ",".join(classes)


def rule_class(text: str) -> str:
    attributes = attrs(text)
    classes = []
    if "simplification" in attributes:
        classes.append("simplification")
    elif "concrete" in attributes:
        classes.append("concrete-equation")
    elif "macro" in attributes or "macro-rec" in attributes:
        classes.append("macro-equation")
    elif "<k>" in text or "<" in text.split("=>", 1)[0]:
        classes.append("operational")
    else:
        classes.append("equational")
    if any(item.startswith("priority(") for item in attributes):
        classes.append("priority")
    if "owise" in attributes:
        classes.append("owise")
    if "functional" in attributes:
        classes.append("functional")
    return ",".join(classes)


counts: Counter[str] = Counter()
per_file: dict[Path, Counter[str]] = {}
records = []

for path in SOURCES:
    relative = (
        path.relative_to("/reference/reference-semantics").as_posix()
        if path.is_relative_to("/reference/reference-semantics")
        else f"candidate/{path.name}"
    )
    file_counts: Counter[str] = Counter()
    for line, kind, text in statements(path):
        classification = kind
        if kind == "syntax":
            classification = syntax_class(text)
        elif kind == "rule":
            classification = rule_class(text)
        elif kind == "claim":
            classification = "reachability-claim"
        records.append((relative, line, kind, classification, text))
        file_counts[kind] += 1
        counts[kind] += 1
        for item in classification.split(","):
            counts[f"class:{item}"] += 1
            file_counts[f"class:{item}"] += 1
    per_file[path] = file_counts

print("# Exhaustive K source inventory")
print()
print("Generated directly from the trusted supplied semantics plus candidate verification/spec sources.")
print()
print("## Summary")
print()
print(f"- Files: {len(SOURCES)}")
print(f"- Syntax declarations: {counts['syntax']}")
print(f"- Rules: {counts['rule']}")
print(f"- Claims: {counts['claim']}")
print(f"- Configurations: {counts['configuration']}")
print(f"- Context declarations: {counts['context']}")
print(f"- Function declarations: {counts['class:function']}")
print(f"- Total declarations: {counts['class:total']}")
print(f"- Functional declarations/rules: {counts['class:functional']}")
print(f"- Opaque-in-proof symbol declarations: {counts['class:opaque-in-proof']}")
print(f"- Priority rules: {counts['class:priority']}")
print(f"- Ordinary operational rules: {counts['class:operational'] - counts['class:priority']}")
print(f"- Equational rules: {counts['class:equational']}")
print(f"- Concrete-only equations: {counts['class:concrete-equation']}")
print(f"- Macro equations: {counts['class:macro-equation']}")
print(f"- Simplification rules: {counts['class:simplification']}")
print()
print("## Per-file counts")
print()
for path in SOURCES:
    relative = (
        path.relative_to("/reference/reference-semantics").as_posix()
        if path.is_relative_to("/reference/reference-semantics")
        else f"candidate/{path.name}"
    )
    c = per_file[path]
    print(
        f"- `{relative}`: syntax={c['syntax']}, rules={c['rule']}, "
        f"claims={c['claim']}, priority={c['class:priority']}, "
        f"simplification={c['class:simplification']}, "
        f"opaque={c['class:opaque-in-proof']}"
    )
print()
print("## Complete declaration and rule listing")
print()
for relative, line, kind, classification, body in records:
    compact = " ".join(
        part.strip()
        for part in body.splitlines()
        if part.strip() and not part.lstrip().startswith("//")
    )
    print(f"- `{relative}:{line}` — **{classification}** — `{compact}`")
