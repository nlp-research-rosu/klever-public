#!/usr/bin/env python3
"""Source-level inventory of all supplied semantics and proof-local K sentences."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/review/candidate-src")
sources = [ROOT / "reference-semantics" / "semantics.k"]
sources += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
sources += [
    ROOT / "verification.k",
    ROOT / "spec.k",
    ROOT / "slice-lemma-spec.k",
]

start_re = re.compile(
    r"^(?:"
    r"(?P<requires>requires)\b"
    r"|(?P<indented>\s*(?:module|endmodule|configuration|syntax|context|rule|claim|alias))\b"
    r")"
)


def sentences(path: Path):
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            token = match.group("requires") or match.group("indented").strip()
            starts.append((index, token))
    for n, (start, kind) in enumerate(starts):
        stop = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        body = lines[start:stop]
        while body and (not body[-1].strip() or body[-1].lstrip().startswith("//")):
            body.pop()
        yield kind, start + 1, start + len(body), "\n".join(body)


attribute_names = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "macro",
    "strict",
    "seqstrict",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "anywhere",
]

global_counts = collections.Counter()
attribute_counts = collections.Counter()
opaque_declarations = []
priority_rules = []
simplification_rules = []

print("INVENTORY_ROOT=", ROOT)
for path in sources:
    relative = path.relative_to(ROOT)
    records = list(sentences(path))
    file_counts = collections.Counter(kind for kind, *_ in records)
    print(f"\nFILE {relative}")
    print("COUNTS", " ".join(f"{k}={v}" for k, v in sorted(file_counts.items())))
    for sequence, (kind, start, stop, body) in enumerate(records, 1):
        global_counts[kind] += 1
        uncommented = "\n".join(line.split("//", 1)[0] for line in body.splitlines())
        attrs = [
            name
            for name in attribute_names
            if re.search(rf"\b{re.escape(name)}\b", uncommented)
        ]
        for attr in attrs:
            attribute_counts[attr] += 1
        label = ",".join(attrs) if attrs else "ordinary"
        print(f"\n[{relative}:{start}-{stop}] kind={kind} attributes={label}")
        print(body)
        if kind == "syntax" and ("no-evaluators" in attrs):
            opaque_declarations.append((relative, start, stop, body))
        if kind == "rule" and "priority" in attrs:
            priority_rules.append((relative, start, stop, body))
        if kind == "rule" and "simplification" in attrs:
            simplification_rules.append((relative, start, stop, body))

print("\nGLOBAL_COUNTS", " ".join(f"{k}={v}" for k, v in sorted(global_counts.items())))
print(
    "ATTRIBUTE_COUNTS",
    " ".join(f"{k}={v}" for k, v in sorted(attribute_counts.items())),
)
print(f"EXPLICIT_NO_EVALUATORS_DECLARATIONS={len(opaque_declarations)}")
for path, start, stop, body in opaque_declarations:
    print(f"OPAQUE [{path}:{start}-{stop}] {body.splitlines()[0].strip()}")
print(f"PRIORITY_RULES={len(priority_rules)}")
for path, start, stop, body in priority_rules:
    print(f"PRIORITY [{path}:{start}-{stop}] {body.splitlines()[0].strip()}")
print(f"SIMPLIFICATION_RULES={len(simplification_rules)}")
for path, start, stop, body in simplification_rules:
    print(f"SIMPLIFICATION [{path}:{start}-{stop}] {body.splitlines()[0].strip()}")
