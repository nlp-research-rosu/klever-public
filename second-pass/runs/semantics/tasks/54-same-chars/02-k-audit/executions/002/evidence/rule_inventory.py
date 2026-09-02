#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


REFERENCE = Path("/reference/reference-semantics")
CANDIDATE_FILES = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
FILES = [REFERENCE / "semantics.k", *sorted((REFERENCE / "semantics").glob("*.k")), *CANDIDATE_FILES]

START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")

# This is the complete fixed-semantics rule slice reachable from #sameChars for
# arbitrary IntSeq inputs. Syntax declarations are separately mapped in REVIEW.md.
USED_RULE_LINES = {
    "semantics/core.k": {
        69, 70,                 # isRefV (guards fixed call behavior)
        101, 102,               # isKwV (call values stay untagged)
        110, 111,               # parameter-name membership total helper
        131, 132, 152,          # lexical/builtin lookup
        158,                    # builtinsScope
        189, 190, 191,          # left-to-right argument evaluation
        214, 215,               # appendVal
    },
    "semantics/operators.k": {17},
    "semantics/functions.k": {63, 64, 78, 85},
    "semantics/builtins.k": {41},
    "semantics/call.k": {20, 21, 31, 52, 53, 69},
    "semantics/set.k": {12, 13, 18, 19, 20, 22, 26, 27, 32, 33, 36, 39},
}


def relative(path: Path) -> str:
    if path.is_relative_to(REFERENCE):
        return path.relative_to(REFERENCE).as_posix()
    return f"candidate/{path.name}"


def block_inventory(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    result = []
    for position, (index, kind) in enumerate(starts):
        limit = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[index:limit]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or block_lines[-1].strip() in {"endmodule"}
        ):
            block_lines.pop()
        text = " ".join(line.strip() for line in block_lines)
        text = re.sub(r"\s+", " ", text)
        result.append(
            {
                "file": relative(path),
                "line": index + 1,
                "kind": kind,
                "text": text,
                "attrs": ",".join(
                    attr
                    for attr, pattern in [
                        ("function", r"\bfunction\b"),
                        ("functional", r"\bfunctional\b"),
                        ("total", r"\btotal\b"),
                        ("macro", r"\bmacro(?:-rec)?\b"),
                        ("opaque/no-evaluators", r"\bno-evaluators\b"),
                        ("symbol", r"\bsymbol\s*\("),
                        ("priority", r"\bpriority\s*\("),
                        ("simplification", r"\bsimplification\b"),
                        ("concrete", r"\bconcrete\b"),
                        ("owise", r"\bowise\b"),
                        ("strictness", r"\b(?:seq)?strict\b"),
                    ]
                    if re.search(pattern, text)
                )
                or "-",
            }
        )
    return result


records = [record for path in FILES for record in block_inventory(path)]
counts = collections.Counter(str(record["kind"]) for record in records)
attribute_counts: collections.Counter[str] = collections.Counter()

print("# Exhaustive K declaration and rule inventory")
print()
print("Sources: trusted supplied semantics tree, candidate verification.k, candidate spec.k.")
print(f"files={len(FILES)} records={len(records)}")
print("kind_counts=" + ",".join(f"{key}:{counts[key]}" for key in sorted(counts)))
print()
print("| ID | source | kind | attributes | proof-slice assessment | declaration/rule |")
print("|---:|---|---|---|---|---|")

for identifier, record in enumerate(records, 1):
    attrs = str(record["attrs"])
    for attr in attrs.split(","):
        if attr != "-":
            attribute_counts[attr] += 1
    file = str(record["file"])
    line = int(record["line"])
    kind = str(record["kind"])
    if file == "candidate/verification.k":
        assessment = "USED-SOUND exact-body launcher" if kind == "rule" else "USED declaration"
    elif file == "candidate/spec.k":
        assessment = "TARGET result-constraining claim" if kind == "claim" else "TARGET declaration"
    elif kind == "rule" and line in USED_RULE_LINES.get(file, set()):
        assessment = "USED-SOUND fixed semantics"
    elif "opaque/no-evaluators" in attrs:
        assessment = "UNUSED opaque boundary"
    elif file == "semantics/concrete.k":
        assessment = "RUNTIME-ONLY; not imported by proof module"
    else:
        assessment = "UNUSED/INERT for submitted proof term"
    text = str(record["text"]).replace("|", "&#124;")
    print(f"| {identifier} | `{file}:{line}` | {kind} | {attrs} | {assessment} | `{text}` |")

print()
print("attribute_counts=" + ",".join(f"{key}:{attribute_counts[key]}" for key in sorted(attribute_counts)))
print("used_rule_locations=")
for file, lines in sorted(USED_RULE_LINES.items()):
    print(f"  {file}: {','.join(str(line) for line in sorted(lines))}")
