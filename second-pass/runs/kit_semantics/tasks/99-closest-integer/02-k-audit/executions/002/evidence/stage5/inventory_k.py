#!/usr/bin/env python3
"""Emit a source-derived inventory of all supplied and candidate K declarations."""

import collections
import re
from pathlib import Path

files = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

start_re = re.compile(r"^\s{2}(syntax|configuration|context|rule|claim)\b")
module_re = re.compile(r"^\s*module\s+(\S+)")

total = collections.Counter()
opaque = []
priority = []
simplification = []
all_entries = []

for path in files:
    lines = path.read_text().splitlines()
    module = None
    for line in lines:
        match = module_re.match(line)
        if match:
            module = match.group(1)
            break
    entries = []
    i = 0
    while i < len(lines):
        match = start_re.match(lines[i])
        if not match:
            i += 1
            continue
        kind = match.group(1)
        start = i
        i += 1
        while i < len(lines):
            if start_re.match(lines[i]) or re.match(r"^\s*endmodule\b", lines[i]):
                break
            i += 1
        raw = "\n".join(lines[start:i]).rstrip()
        normalized = " ".join(
            piece.strip()
            for piece in raw.splitlines()
            if piece.strip() and not piece.lstrip().startswith("//")
        )
        entry = {
            "path": str(path),
            "module": module,
            "kind": kind,
            "line": start + 1,
            "end_line": i,
            "normalized": normalized,
            "raw": raw,
        }
        entries.append(entry)
        all_entries.append(entry)
        total[kind] += 1
        if "no-evaluators" in raw or (
            kind == "syntax"
            and "[function" in raw
            and not any(
                re.search(rf"\brule\s+{re.escape(name)}\s*\(", text)
                for name in re.findall(r"\b([A-Za-z][A-Za-z0-9]*)\s*\(", raw)
                for text in lines
            )
        ):
            opaque.append(entry)
        if "priority(" in raw:
            priority.append(entry)
        if "simplification" in raw:
            simplification.append(entry)

    counts = collections.Counter(e["kind"] for e in entries)
    print(
        f"FILE {path} module={module} "
        + " ".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
    )
    for entry in entries:
        attrs = re.findall(r"\[([^\]]+)\]", entry["raw"])
        attr_text = "; ".join(attrs) if attrs else "-"
        text = entry["normalized"]
        if len(text) > 1200:
            text = text[:1200] + " ...[bounded]"
        print(
            f"  {entry['kind'].upper()} {entry['line']}-{entry['end_line']} "
            f"attrs={attr_text} :: {text}"
        )

print("TOTALS " + " ".join(f"{kind}={total[kind]}" for kind in sorted(total)))
print(f"OPAQUE_OR_UNEVALUATED_COUNT {len(opaque)}")
for entry in opaque:
    print(
        f"  {entry['path']}:{entry['line']} {entry['normalized'][:1000]}"
    )
print(f"PRIORITY_DECLARATION_COUNT {len(priority)}")
for entry in priority:
    print(
        f"  {entry['path']}:{entry['line']} {entry['normalized'][:1000]}"
    )
print(f"SIMPLIFICATION_DECLARATION_COUNT {len(simplification)}")
for entry in simplification:
    print(
        f"  {entry['path']}:{entry['line']} {entry['normalized'][:1000]}"
    )
