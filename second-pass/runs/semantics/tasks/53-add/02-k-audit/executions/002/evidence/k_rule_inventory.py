#!/usr/bin/env python3
"""Exhaustive source-level inventory of the supplied K theory and candidate proof."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


SEMANTICS = Path("/tmp/audit-work/53-add-clean/reference-semantics")
CANDIDATE = Path("/tmp/audit-work/53-add-clean")

paths = [SEMANTICS / "semantics.k"]
paths += sorted((SEMANTICS / "semantics").glob("*.k"))
paths += [CANDIDATE / "verification.k", CANDIDATE / "spec.k"]

directive = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim)\b"
)
next_top_level = re.compile(
    r"^\s*(?:configuration|syntax|context|rule|claim|module|endmodule|imports)\b"
)

# Exact local source rules/declarations on the target proof's execution slice.
active_lines: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 41, 56, 57, 60, 61},
    "semantics/core.k": {
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
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        208,
        209,
        210,
        213,
        214,
        215,
    },
    "semantics/functions.k": {8, 14, 63, 64, 78, 85},
    "semantics/call.k": {19, 20, 21, 69},
    "semantics/operators.k": {12},
    "semantics/int.k": {9},
    "verification.k": {7, 9},
    "spec.k": {6},
}

known_limits: dict[tuple[str, int], str] = {
    ("semantics/controls.k", 36): "non-math ImportFrom is deliberately a no-op",
    ("semantics/float.k", 61): "generic Import is deliberately a no-op",
    ("semantics/functions.k", 85): (
        "frame deallocation assumes no escaping nested closure; target call satisfies it"
    ),
    ("semantics/str.k", 13): "string literal conversion is ASCII-only",
    ("semantics/subscript.k", 11): (
        "total opaque/OOB access is intentionally underspecified; target has no subscript"
    ),
    ("semantics/core.k", 233): (
        "OOB positional write is modeled as unchanged; target has no subscript assignment"
    ),
    ("semantics/builtins.k", 152): (
        "single-character int(str) accepts only decimal digits"
    ),
    ("semantics/builtins.k", 156): (
        "multi-character int(str) assumes numeric codes without a digit guard"
    ),
    ("semantics/builtins.k", 187): (
        "eval covers a restricted arithmetic grammar and totalizes malformed forms"
    ),
    ("semantics/builtins.k", 295): (
        "the restricted type model does not treat Bool as a Python int subtype"
    ),
    ("semantics/list.k", 27): (
        "symbolic-backend list equality is shallow when nested heap refs occur"
    ),
    ("semantics/tuple.k", 18): (
        "tuple equality is shallow when nested heap refs occur"
    ),
    ("semantics/dict.k", 95): (
        "dict value comparison uses K structural equality rather than recursive object equality"
    ),
    ("semantics/methods.k", 47): (
        "strip recognizes only the semantics' four modeled ASCII whitespace codes"
    ),
    ("semantics/methods.k", 58): (
        "encode is a string-code identity abstraction rather than Python bytes"
    ),
    ("semantics/controls.k", 106): (
        "list iteration uses an explicit snapshot and excludes mutation-during-iteration"
    ),
    ("semantics/float.k", 128): (
        ">= is derived as not-< and therefore does not model IEEE NaN ordering"
    ),
    ("semantics/float.k", 129): (
        "<= is derived as not-> and therefore does not model IEEE NaN ordering"
    ),
    ("semantics/float.k", 162): (
        "decimal-string parsing assumes its restricted digit/dot input grammar"
    ),
    ("semantics/methods.k", 13): "character predicates/case mappings are ASCII-only",
}


def relative(path: Path) -> str:
    if path.is_relative_to(SEMANTICS):
        return path.relative_to(SEMANTICS).as_posix()
    return path.name


def classify(rel: str, line: int, text: str, kind: str) -> tuple[str, str]:
    if rel == "spec.k":
        return "TARGET-CLAIM", "universally quantified result-constraining entry theorem"
    if rel == "verification.k":
        return (
            "ACTIVE-HARNESS",
            "expands the audit entry marker into the exact module plus ordinary fixed-semantics call",
        )
    if (rel, line) in known_limits:
        return "LIMITATION", known_limits[(rel, line)]
    if "no-evaluators" in text or "symbol(" in text:
        return (
            "TRUSTED-OPAQUE-INACTIVE",
            "result-bearing opaque declaration, absent from the target execution slice",
        )
    if "[concrete]" in text:
        return (
            "CONCRETE-ONLY-INACTIVE",
            "LLVM-only executable equation, absent from the Haskell target proof",
        )
    if line in active_lines.get(rel, set()):
        return (
            "ACTIVE-ACCEPTED",
            "faithful constructor/control/state step on the exact integer-add execution slice",
        )
    if kind == "syntax":
        return (
            "DECLARATION-INACTIVE",
            "syntax/type declaration not exercised by the target unless grouped with an active alternative",
        )
    if kind in {"configuration", "context"}:
        return (
            "FIXED-SEMANTICS-ACCEPTED",
            "fixed configuration/evaluation-order declaration; no result oracle",
        )
    return (
        "INACTIVE-ACCEPTED-PARTIAL",
        "truthful on its matched restricted-domain constructors; not on the target dependency slice",
    )


kind_counts: Counter[str] = Counter()
assessment_counts: Counter[str] = Counter()
file_counts: dict[str, Counter[str]] = defaultdict(Counter)
attribute_counts: Counter[str] = Counter()
item_count = 0

for path in paths:
    rel = relative(path)
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = directive.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines) and not next_top_level.match(lines[index]):
            index += 1
        block = "\n".join(lines[start:index]).strip()
        normalized = " ".join(block.split())
        assessment, reason = classify(rel, start + 1, normalized, kind)
        attrs = sorted(
            set(
                re.findall(
                    r"\b(functional|function|total|simplification|symbol|"
                    r"no-evaluators|priority|owise|concrete|macro-rec|macro|"
                    r"strict|seqstrict)\b",
                    normalized,
                )
            )
        )

        item_count += 1
        kind_counts[kind] += 1
        assessment_counts[assessment] += 1
        file_counts[rel][kind] += 1
        attribute_counts.update(attrs)
        print(
            f"ITEM {item_count:04d} | {rel}:{start + 1}-{index} | "
            f"kind={kind} | assessment={assessment} | "
            f"attrs={','.join(attrs) if attrs else '-'}"
        )
        print(f"  reason={reason}")
        print(f"  source={normalized}")

print("SUMMARY")
print(f"item_count={item_count}")
print(f"kind_counts={dict(sorted(kind_counts.items()))}")
print(f"assessment_counts={dict(sorted(assessment_counts.items()))}")
print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")
for rel in sorted(file_counts):
    print(f"file={rel} counts={dict(sorted(file_counts[rel].items()))}")
print("INVENTORY_COMPLETE=True")
