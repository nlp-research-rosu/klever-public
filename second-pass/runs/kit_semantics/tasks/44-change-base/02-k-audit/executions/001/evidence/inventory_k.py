#!/usr/bin/env python3
import re
from collections import Counter, defaultdict
from pathlib import Path


paths = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

declaration = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|priority)\b"
)
boundary = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|priority|module|endmodule|imports)\b"
)

overall = Counter()
per_file = defaultdict(Counter)
items = []

for path in paths:
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if declaration.match(line) and not line.lstrip().startswith("//")
    ]
    for ordinal, start in enumerate(starts):
        match = declaration.match(lines[start])
        assert match is not None
        kind = match.group(1)
        stop = len(lines)
        for index in range(start + 1, len(lines)):
            if boundary.match(lines[index]) and not lines[index].lstrip().startswith("//"):
                stop = index
                break
        raw = "\n".join(lines[start:stop]).strip()
        compact = " ".join(
            line.strip()
            for line in raw.splitlines()
            if line.strip() and not line.lstrip().startswith("//")
        )
        attributes = []
        for name, pattern in [
            ("function", r"\bfunction\b"),
            ("functional", r"\bfunctional\b"),
            ("total", r"\btotal\b"),
            ("opaque/no-evaluators", r"\bno-evaluators\b"),
            ("priority", r"\bpriority\s*\("),
            ("simplification", r"\bsimplification\b"),
            ("concrete", r"\bconcrete\b"),
            ("owise", r"\bowise\b"),
            ("macro", r"\bmacro(?:-rec)?\b"),
            ("strict", r"\b(?:seq)?strict\b"),
        ]:
            if re.search(pattern, raw):
                attributes.append(name)
        category = kind
        if kind == "rule":
            if "simplification" in attributes:
                category = "rule:simplification"
            elif "concrete" in attributes:
                category = "rule:concrete"
            elif "priority" in attributes:
                category = "rule:priority"
            else:
                category = "rule:ordinary"
        overall[category] += 1
        per_file[path][category] += 1
        items.append(
            (
                path,
                start + 1,
                kind,
                ",".join(attributes) if attributes else "-",
                compact,
            )
        )

print("INVENTORY_SCOPE")
for path in paths:
    print(path)
print(f"TOTAL_ITEMS={len(items)}")
print(f"OVERALL_COUNTS={dict(sorted(overall.items()))}")
for path in paths:
    print(f"FILE_COUNTS {path}: {dict(sorted(per_file[path].items()))}")

print("INVENTORY_ITEMS")
for number, (path, line, kind, attributes, compact) in enumerate(items, 1):
    print(
        f"{number:04d} {path}:{line} kind={kind} "
        f"attributes={attributes} :: {compact}"
    )
