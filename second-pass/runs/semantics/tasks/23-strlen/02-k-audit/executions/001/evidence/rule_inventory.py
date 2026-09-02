#!/usr/bin/env python3
"""Create a line-addressed exhaustive inventory of local K constructs."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/tmp/audit-work/23-strlen/candidate")
OUTPUT = Path("/audit-output/evidence/11-rule-inventory.md")

sources = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

directive_re = re.compile(r"^\s*(syntax|configuration|context|rule|claim)\b")
boundary_re = re.compile(
    r"(?:^\s*(?:syntax|configuration|context|rule|claim|imports)\b)"
    r"|(?:^(?:module|endmodule|requires)\b)"
)
attribute_names = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "concrete",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "simplification",
)

# Rules on the exact symbolic execution path for this submitted program.
used_rule_rationales: dict[tuple[str, int], str] = {
    ("semantics/core.k", 125): "opens the exact Module and exposes its statements",
    ("semantics/core.k", 126): "sequences the single FuncDef statement",
    ("semantics/core.k", 127): "eliminates the empty statement tail",
    ("semantics/core.k", 131): "starts lookup of strlen, len, and string in the active scope",
    ("semantics/core.k", 132): "returns each found strlen/len/string binding",
    ("semantics/core.k", 152): "walks from call scope to module and builtin parents",
    ("semantics/core.k", 158): "defines the fixed builtin frame containing len",
    ("semantics/core.k", 189): "evaluates the one argument left-to-right",
    ("semantics/core.k", 190): "accumulates the evaluated string argument",
    ("semantics/core.k", 191): "dispatches after the final argument",
    ("semantics/core.k", 228): "base case for structural string length",
    ("semantics/core.k", 229): "inductive case for structural string length",
    ("semantics/builtins.k", 21): "routes builtin len to seqLen",
    ("semantics/builtins.k", 24): "routes a str value to isLen",
    ("semantics/call.k", 20): "evaluates each real Call node's callee",
    ("semantics/call.k", 21): "evaluates real call arguments after the callee",
    ("semantics/call.k", 31): "dispatches the len builtin after higher-priority folds do not match",
    ("semantics/call.k", 69): "enters the real strlen closure, installs frame and continuation",
    ("semantics/functions.k", 14): "loads the real FuncDef body into module scope",
    ("semantics/functions.k", 63): "finishes parameter binding",
    ("semantics/functions.k", 64): "binds string to the supplied str argument",
    ("semantics/functions.k", 78): "implements the real Return and discards only callee-local tail",
    ("semantics/functions.k", 85): "returns isLen(S), restores caller state, and removes call frame",
    ("verification.k", 8): "macro expands to the exact submitted constructor tree",
    ("verification.k", 19): "fresh harness symbol loads that tree then calls its public entry point",
}

opaque_attrs = {"symbol", "no-evaluators"}
counters: Counter[str] = Counter()
file_counters: dict[str, Counter[str]] = defaultdict(Counter)
records: list[dict[str, object]] = []

for source in sources:
    rel = (
        str(source.relative_to(ROOT / "reference-semantics"))
        if "reference-semantics" in source.parts
        else source.name
    )
    lines = source.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        match = directive_re.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index + 1
        block = [lines[index].strip()]
        cursor = index + 1
        while cursor < len(lines) and not boundary_re.match(lines[cursor]):
            stripped = lines[cursor].strip()
            if stripped and not stripped.startswith("//"):
                block.append(stripped)
            cursor += 1
        text = " ".join(block)
        attrs = [name for name in attribute_names if re.search(rf"\b{re.escape(name)}\b", text)]
        key = (rel, start)
        if kind == "rule" and key in used_rule_rationales:
            review = f"USED_FIXED_SOUND — {used_rule_rationales[key]}"
        elif kind == "rule" and source.name == "verification.k":
            review = "PROOF_LOCAL_REVIEW_REQUIRED"
        elif kind == "rule":
            review = (
                "FIXED_UNUSED_OPAQUE"
                if opaque_attrs.intersection(attrs)
                else "FIXED_UNUSED"
            )
        elif kind == "claim":
            review = "TARGET_CLAIM"
        else:
            review = "DECLARATION"
        records.append(
            {
                "file": rel,
                "line": start,
                "kind": kind,
                "attrs": attrs,
                "review": review,
                "text": text,
            }
        )
        counters[kind] += 1
        file_counters[rel][kind] += 1
        for attr in attrs:
            counters[f"attr:{attr}"] += 1
            file_counters[rel][f"attr:{attr}"] += 1
        index = cursor

with OUTPUT.open("w", encoding="utf-8") as out:
    out.write("# Exhaustive local K construct inventory\n\n")
    out.write(
        "Generated from the fresh scratch source. `USED_FIXED_SOUND` identifies "
        "rules exercised by the strlen claim. `FIXED_UNUSED` and "
        "`FIXED_UNUSED_OPAQUE` identify supplied-semantics rules that cannot "
        "match any term on this program's path; they are not proof-local axioms. "
        "Substantive decisions and trust-boundary analysis are in REVIEW.md.\n\n"
    )
    out.write("## Totals\n\n")
    for key in sorted(counters):
        out.write(f"- {key}: {counters[key]}\n")
    out.write("\n## Per-file counts\n\n")
    for rel in sorted(file_counters):
        rendered = ", ".join(
            f"{key}={value}" for key, value in sorted(file_counters[rel].items())
        )
        out.write(f"- `{rel}`: {rendered}\n")
    out.write("\n## Items\n\n")
    for number, record in enumerate(records, start=1):
        attrs = ", ".join(record["attrs"]) if record["attrs"] else "none"
        text = str(record["text"]).replace("|", "\\|")
        out.write(
            f"{number}. `{record['file']}:{record['line']}` "
            f"kind=`{record['kind']}` attrs=`{attrs}` "
            f"review=`{record['review']}`\n\n"
            f"   `{text}`\n\n"
        )

print(f"sources={len(sources)}")
print(f"records={len(records)}")
for key in sorted(counters):
    print(f"{key}={counters[key]}")
print(f"output={OUTPUT}")
