#!/usr/bin/env python3
"""Line-addressed inventory of all K declarations, rules, claims, and attributes."""

from pathlib import Path
import hashlib
import re


WORK = Path("/tmp/audit-work/124-valid-date")
files = sorted((WORK / "reference-semantics").rglob("*.k"))
files.extend((WORK / name) for name in ("verification.k", "spec.k", "audit-false-result.k"))

declaration = re.compile(r"^\s*(syntax|configuration|context|rule|claim)\b")
attribute = re.compile(
    r"\[(?:[^\]]*\b(?:function|functional|total|simplification|concrete|"
    r"priority|owise|macro|strict|seqstrict|symbol|no-evaluators|hook)\b[^\]]*)\]"
)

for path in files:
    data = path.read_bytes()
    text = data.decode("utf-8")
    lines = text.splitlines()
    rel = path.relative_to(WORK)
    decls = []
    attrs = []
    for line_number, line in enumerate(lines, 1):
        if declaration.search(line):
            decls.append((line_number, line.strip()))
        if attribute.search(line):
            attrs.append((line_number, line.strip()))
    print(
        f"FILE {rel} sha256={hashlib.sha256(data).hexdigest()} "
        f"lines={len(lines)} declarations={len(decls)} attribute_lines={len(attrs)}"
    )
    for line_number, line in decls:
        print(f"  DECL {line_number}: {line}")
    for line_number, line in attrs:
        print(f"  ATTR {line_number}: {line}")
