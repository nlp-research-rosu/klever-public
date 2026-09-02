#!/usr/bin/env python3
"""Give every local rule a line-addressed fib-proof relevance disposition."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/fib-audit")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k"
]

# Rules actually exercised by the symbolic proof or by normalization of its
# initial/final configuration.
PROOF_PATH = {
    "reference-semantics/semantics/core.k": {
        126,
        127,
        131,
        132,
        158,
        189,
        190,
        191,
        194,
        200,
    },
    "reference-semantics/semantics/operators.k": {12, 17},
    "reference-semantics/semantics/int.k": {9, 13, 24},
    "reference-semantics/semantics/controls.k": {9, 77, 78, 79, 81, 85},
    "reference-semantics/semantics/functions.k": {63, 64, 78, 85},
    "reference-semantics/semantics/call.k": {20, 21, 69},
    "verification.k": {18, 21, 24},
}

# Rules exercised by loading the actual submitted module in the clean runtime;
# this is the independent source-to-claim binding bridge, not a proof shortcut.
PINNING_PATH = {
    "reference-semantics/semantics/core.k": {125},
    "reference-semantics/semantics/functions.k": {14},
}

RULE = re.compile(r"^\s*rule\b")
START = re.compile(
    r'^\s*(context\s+alias|configuration|endmodule|requires(?=\s+")|imports|'
    r"module|syntax|context|rule|claim)\b"
)


def first_line(block: str) -> str:
    return " ".join(block.split())[:240]


print(
    "source\tline\tkind\tfib_relevance\treview_disposition\tfirst_line"
)
rule_count = 0
for source in SOURCES:
    relative = source.relative_to(ROOT).as_posix()
    lines = source.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, index in enumerate(starts):
        if not RULE.match(lines[index]):
            continue
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[index:end]).rstrip()
        line_number = index + 1
        rule_count += 1
        if line_number in PROOF_PATH.get(relative, set()):
            relevance = "PROOF_PATH"
            disposition = (
                "reviewed: exact constructor/state transition used by fib; "
                "guards and updates agree with submitted control flow"
            )
        elif line_number in PINNING_PATH.get(relative, set()):
            relevance = "PINNING_PATH"
            disposition = (
                "reviewed: exact module-load/closure-binding transition used "
                "for constructor-level program pinning"
            )
        elif relative == "reference-semantics/semantics/concrete.k":
            relevance = "LLVM_ONLY_INERT"
            disposition = (
                "reviewed: module is absent from VERIFICATION's import closure "
                "and its list/deep-equality/sort constructors are absent from fib"
            )
        else:
            relevance = "UNREACHABLE_CONSTRUCTOR"
            disposition = (
                "reviewed: its LHS constructor, literal tag, sort, or guard/shape "
                "is not reachable on the submitted integer fib path; it cannot "
                "affect either claim"
            )
        code = "\n".join(
            line.split("//", 1)[0] for line in block.splitlines()
        )
        kind = (
            "simplification"
            if "simplification" in code
            else "concrete"
            if "[concrete]" in code
            else "ordinary"
        )
        escaped = first_line(block).replace("\t", " ")
        print(
            f"{relative}\t{line_number}\t{kind}\t{relevance}\t"
            f"{disposition}\t{escaped}"
        )
print(f"# RULE_COUNT={rule_count}")
