#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


roots = [
    Path("/candidate/reference-semantics/semantics.k"),
    *sorted(Path("/candidate/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

item_re = re.compile(
    r"^(?P<indent>[ \t]*)(?P<kind>syntax|rule|claim|context|configuration)\b"
)
tag_names = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "macro",
    "macro-rec",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "strict",
    "seqstrict",
    "hook",
]

items = []
for path in roots:
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = item_re.match(line)
        if match and len(match.group("indent").expandtabs(8)) <= 2:
            starts.append((index, match.group("kind")))
    for pos, (start, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        # Stop before an unindented module boundary if it precedes the next
        # declaration.
        for index in range(start + 1, end):
            if re.match(r"^(?:module|endmodule)\b", lines[index]):
                end = index
                break
        text = "\n".join(lines[start:end]).rstrip()
        code_text = "\n".join(
            re.sub(r"//.*$", "", line).rstrip() for line in text.splitlines()
        ).strip()
        tags = []
        for tag in tag_names:
            if re.search(rf"\b{re.escape(tag)}(?:\b|\()", code_text):
                tags.append(tag)
        if kind == "rule":
            tags.append("operational" if "<k>" in code_text else "equation-or-macro")
        items.append(
            {
                "path": path,
                "line": start + 1,
                "kind": kind,
                "tags": tags,
                "text": code_text,
            }
        )

counts = Counter(item["kind"] for item in items)
tag_counts = Counter(tag for item in items for tag in item["tags"])
print("# Exhaustive K declaration and rule inventory")
print()
print("Source scope: supplied `reference-semantics/semantics.k`, every supplied")
print("`reference-semantics/semantics/*.k` helper, `verification.k`, and `spec.k`.")
print()
print(
    "Counts: "
    + ", ".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
    + f", total_items={len(items)}"
)
print(
    "Attribute/category counts: "
    + ", ".join(f"{tag}={tag_counts[tag]}" for tag in tag_names + ["operational", "equation-or-macro"])
)
print()

current = None
for number, item in enumerate(items, 1):
    rel = str(item["path"]).replace("/candidate/", "")
    if rel != current:
        current = rel
        print(f"## {rel}")
        print()
    tag_text = ", ".join(item["tags"]) if item["tags"] else "none"
    first_line = " ".join(item["text"].split())
    print(
        f"{number:04d}. `{item['kind']}` line {item['line']}; "
        f"tags: {tag_text}; `{first_line}`"
    )

expected = {
    "syntax": 228,
    "rule": 696,
    "claim": 1,
    "context": 5,
    "configuration": 1,
}
if dict(counts) != expected:
    print()
    print(f"COUNT_MISMATCH actual={dict(counts)} expected={expected}")
    raise SystemExit(1)
