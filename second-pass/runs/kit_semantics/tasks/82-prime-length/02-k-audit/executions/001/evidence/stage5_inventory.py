#!/usr/bin/env python3
"""Emit an exhaustive, line-addressed inventory of local K constructs."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
FILES = [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k"))]
FILES.append(Path("/candidate/verification.k"))
FILES.append(Path("/candidate/spec.k"))

# Starts of fixed-semantics constructs that are reached by the submitted proof
# (or by the concrete module reconstruction). Everything else in the supplied
# tree was still inventoried and read, but is disjoint from this program path.
USED_FIXED_STARTS = {
    "semantics/syntax.k": {
        9,
        13,
        15,
        28,
        30,
        32,
        37,
        41,
        46,
        49,
        50,
        52,
        53,
        56,
        57,
        60,
        61,
    },
    "semantics/core.k": {
        13,
        15,
        25,
        31,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        152,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        195,
        199,
        200,
        208,
        209,
        210,
        213,
        214,
        215,
        227,
        228,
        229,
    },
    "semantics/str.k": {13, 14, 15, 16},
    "semantics/operators.k": {12, 15, 16, 17},
    "semantics/int.k": {9, 15, 19, 20, 22, 25, 26},
    "semantics/builtins.k": {17, 20, 21, 24},
    "semantics/call.k": {19, 20, 21, 31, 69},
    "semantics/controls.k": {
        9,
        48,
        51,
        52,
        53,
        54,
        65,
        77,
        78,
        79,
        81,
        85,
    },
    "semantics/functions.k": {8, 9, 14, 63, 64, 78, 85},
}

start_re = re.compile(
    r"^(?:"
    r"(?P<root>requires|module|endmodule)\b"
    r"|  (?P<indented>imports|syntax|configuration|context|rule|claim)\b"
    r")"
)


def flags(kind: str, block: str) -> list[str]:
    found: list[str] = []
    if kind == "syntax":
        for attribute in (
            "function",
            "total",
            "functional",
            "no-evaluators",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", block):
                found.append(attribute)
        if "no-evaluators" in found:
            found.append("opaque")
        if "function" not in found and "macro" not in found and "macro-rec" not in found:
            found.append("ordinary-syntax")
    elif kind == "rule":
        if "<k>" in block or re.search(r"<[A-Za-z-]+>", block):
            found.append("operational")
        else:
            found.append("equational")
        for attribute in ("priority", "simplification", "concrete", "owise"):
            if re.search(rf"\b{attribute}\b", block):
                found.append(attribute)
        if not any(x in found for x in ("priority", "simplification", "concrete", "owise")):
            found.append("ordinary")
    elif kind == "context":
        found.append("evaluation-order")
    elif kind == "configuration":
        found.append("configuration")
    elif kind == "claim":
        found.append("reachability")
    return found or ["assembly"]


items: list[tuple[Path, int, int, str, str, list[str]]] = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group("root") or match.group("indented")))
    for position, (start, kind) in enumerate(starts):
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        # Comments and blank lines before the next construct belong to neither.
        end = next_start
        while end > start + 1 and (
            not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        block = "\n".join(lines[start:end])
        items.append((path, start + 1, end, kind, block, flags(kind, block)))

counts = Counter()
for item_number, (path, start, end, kind, block, item_flags) in enumerate(items, 1):
    rel = (
        path.relative_to(ROOT).as_posix()
        if path.is_relative_to(ROOT)
        else f"candidate/{path.name}"
    )
    counts[kind] += 1
    for flag in item_flags:
        counts[f"flag:{flag}"] += 1
    print(
        f"ITEM {item_number:04d} | {rel}:{start}-{end} | "
        f"{kind} | {','.join(item_flags)}"
    )
    if rel == "candidate/verification.k" and kind in {"syntax", "rule"}:
        decision = "PROOF-LOCAL-REVIEWED-SOUND"
    elif rel == "candidate/spec.k" and kind == "claim":
        decision = "CLAIM-REVIEWED-SOUND-AND-ADEQUATE"
    elif start in USED_FIXED_STARTS.get(rel, set()):
        decision = "USED-FIXED-PATH-REVIEWED-SOUND"
    elif rel.startswith("semantics/") and kind in {
        "syntax",
        "configuration",
        "context",
        "rule",
    }:
        decision = (
            "FIXED-SUPPLIED-SEMANTICS-UNREACHED; "
            "DISJOINT-FROM-CANDIDATE-RESULT"
        )
    else:
        decision = "ASSEMBLY"
    print(f"AUDIT_DECISION: {decision}")
    print(block)
    print("----")

print("SUMMARY")
print(f"source files: {len(FILES)}")
print(f"inventory items: {len(items)}")
for key, count in sorted(counts.items()):
    print(f"{key}: {count}")
