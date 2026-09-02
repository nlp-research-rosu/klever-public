#!/usr/bin/env python3
"""Exhaustive source-location inventory for the supplied and proof-local K."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/tmp/audit-work/prime-length-audit/reference-semantics/semantics.k"),
    *sorted(
        Path("/tmp/audit-work/prime-length-audit/reference-semantics/semantics").glob(
            "*.k"
        )
    ),
    Path("/tmp/audit-work/prime-length-audit/verification.k"),
    Path("/tmp/audit-work/prime-length-audit/spec.k"),
]
START = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim|module|endmodule|imports|requires)\b"
)
ATTR_NAMES = [
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


entries: list[dict[str, object]] = []
for path in ROOTS:
    lines = path.read_text().splitlines()
    for index, line in enumerate(lines):
        match = START.match(line)
        if match is None:
            continue
        end = index + 1
        while end < len(lines):
            if BOUNDARY.match(lines[end]):
                break
            end += 1
        block = "\n".join(lines[index:end])
        code_block = "\n".join(
            source_line.split("//", 1)[0] for source_line in lines[index:end]
        )
        attrs = [
            attr
            for attr in ATTR_NAMES
            if re.search(rf"\b{re.escape(attr)}\b", code_block)
        ]
        entries.append(
            {
                "file": path,
                "line": index + 1,
                "kind": match.group(1),
                "attrs": attrs,
                "block": block,
            }
        )

print("inventory_scope:")
for path in ROOTS:
    print(f"  {path} sha256={sha256(path)}")
print(f"entry_count={len(entries)}")
kind_counts = Counter(str(entry["kind"]) for entry in entries)
print(f"kind_counts={dict(sorted(kind_counts.items()))}")
attr_counts = Counter(
    attr for entry in entries for attr in entry["attrs"]  # type: ignore[union-attr]
)
print(f"attribute_entry_counts={dict(sorted(attr_counts.items()))}")
print("file_counts:")
for path in ROOTS:
    matching = [entry for entry in entries if entry["file"] == path]
    counts = Counter(str(entry["kind"]) for entry in matching)
    print(f"  {path}: total={len(matching)} kinds={dict(sorted(counts.items()))}")

print("opaque_or_symbolic_declarations:")
for entry in entries:
    attrs = entry["attrs"]
    if "no-evaluators" in attrs or "symbol" in attrs:  # type: ignore[operator]
        first = " ".join(str(entry["block"]).split())
        print(
            f"  {entry['file']}:{entry['line']} attrs={','.join(attrs)} "
            f"text={first}"
        )

print("priority_rules:")
for entry in entries:
    if "priority" in entry["attrs"]:  # type: ignore[operator]
        first = " ".join(str(entry["block"]).split())
        print(
            f"  {entry['file']}:{entry['line']} attrs={','.join(entry['attrs'])} "
            f"text={first}"
        )

print("simplification_rules:")
simplifications = [
    entry for entry in entries if "simplification" in entry["attrs"]  # type: ignore[operator]
]
if not simplifications:
    print("  NONE")
for entry in simplifications:
    print(f"  {entry['file']}:{entry['line']} {' '.join(str(entry['block']).split())}")

print("exhaustive_entries:")
for number, entry in enumerate(entries, 1):
    collapsed = " ".join(str(entry["block"]).split())
    if len(collapsed) > 500:
        collapsed = collapsed[:497] + "..."
    source_class = (
        "PROOF_LOCAL"
        if str(entry["file"]).endswith(("verification.k", "spec.k"))
        else "FIXED_SUPPLIED"
    )
    disposition = (
        "REVIEWED_IN_DETAIL"
        if source_class == "PROOF_LOCAL"
        else "FIXED_BASELINE; REACHABILITY_RELEVANCE_REVIEWED"
    )
    print(
        f"{number:04d} {entry['kind'].upper()} {entry['file']}:{entry['line']} "
        f"class={source_class} disposition={disposition} "
        f"attrs={','.join(entry['attrs']) or '-'} text={collapsed}"
    )

print("used_solution_constructor_map:")
used_map = [
    ("Module", "semantics/syntax.k:61", "semantics/core.k:124-127 (#loadAll and sequencing); entry claims instead use an exact closure"),
    ("FuncDef", "semantics/syntax.k:53", "semantics/functions.k:14-16; mechanically replaced by its exact closure in entry claims"),
    ("Params/ParamNames", "semantics/syntax.k:57,60", "semantics/functions.k:63-75 (#bindP)"),
    ("Assign(Name,...)", "semantics/syntax.k:41", "semantics/controls.k:9-18"),
    ("Name", "semantics/syntax.k:12", "semantics/core.k:130-154 (#look)"),
    ("Call", "semantics/syntax.k:28", "semantics/call.k:18-32 and 69-75"),
    ("len", "semantic value from core.k:157-181", "semantics/builtins.k:17-26 (seqLen(str)=isLen)"),
    ("If", "semantics/syntax.k:49", "semantics/controls.k:50-54 plus strict condition evaluation"),
    ("Compare/CmpOp", "semantics/syntax.k:30,32", "semantics/operators.k:14-20 and int.k:22-27"),
    ("Int/Bool", "semantics/syntax.k:9,11", "semantics/core.k:193-196"),
    ("Return", "semantics/syntax.k:50", "semantics/functions.k:77-90"),
    ("While", "semantics/syntax.k:46", "semantics/controls.k:65-82; proof-local interception additionally reviewed"),
    ("BinOp('%',...)", "semantics/syntax.k:15", "semantics/operators.k:12 and int.k:15,19-20"),
    ("AugAssign('+')", "semantics/syntax.k:44", "semantics/controls.k:20-31 and int.k:9"),
    ("Stmts/Exprs lists", "semantics/syntax.k:37,56", "semantics/core.k:123-127,183-191"),
]
for constructor, declaration, rules in used_map:
    print(f"  {constructor}: declaration={declaration}; rules={rules}")

print("proof_local_dispositions:")
for line in [
    "verification.k:8-17 primeLoopBody function/equation: ACCEPT; exact constructor abbreviation.",
    "verification.k:19-31 primeBody function/equation: ACCEPT; exact constructor abbreviation.",
    "verification.k:33-35 primeLengthClosure function/equation: ACCEPT; exact binding, parameters, body, and defining scope.",
    "verification.k:40-42 observation syntax: PROOF-LOCAL MARKERS; result influence through setup claim.",
    "verification.k:43-49 priority(1) While interception: REJECT; context-broad operational bridge, no bridge-free connection theorem, preempts real While semantics.",
    "verification.k:51-56 capture-N continuation rule: REJECT AS BRIDGE COMPONENT; fixed lookup is retained but it serves the unproved interception.",
    "verification.k:58-69 capture-D cleanup rule: REJECT; discards arbitrary REST and fabricates scope/frame cleanup and a marker.",
    "verification.k:73-79 noDivisorsFrom equations: ACCEPT for D>=2 uses; guards are exhaustive/disjoint and recursion descends toward D>=N.",
    "spec.k:9-44 divisor-loop claim: SOUND HELPER; exact #while control state returns noDivisorsFrom(N,D).",
    "spec.k:51-72 prime-length-small claim: SOUND ENTRY SLICE; exact closure returns false for lengths 0 or 1.",
    "spec.k:77-99 prime-length-setup claim: INADEQUATE/BRIDGE-DEPENDENT; reaches an invented marker, not a returned result.",
]:
    print(f"  {line}")
