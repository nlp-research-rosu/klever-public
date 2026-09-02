#!/usr/bin/env python3
"""Exhaustive line-addressed inventory of the submitted K source theory."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/27-flip-case")
FILES = sorted((SCRATCH / "reference-semantics").rglob("*.k")) + [
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]

START = re.compile(
    r"^\s*(requires|module|imports|endmodule|syntax|configuration|context|rule|claim)\b"
)

# Exact handwritten rules exercised by loading, calling, and returning from
# flip_case. Generated heating/cooling follows from the marked strict syntax
# declarations and is represented by those declarations.
USED_RULES = {
    "reference-semantics/semantics/core.k": {
        125,
        126,
        127,
        131,
        132,
        189,
        190,
        191,
    },
    "reference-semantics/semantics/call.k": {16, 20, 21, 24, 69},
    "reference-semantics/semantics/functions.k": {14, 63, 64, 78, 85},
    "reference-semantics/semantics/methods.k": {
        21,
        113,
        116,
        150,
        151,
        152,
        163,
        164,
    },
}

USED_DECLARATIONS = {
    "reference-semantics/semantics/syntax.k": {9, 28, 29, 50, 53, 56, 57, 60, 61},
    "reference-semantics/semantics/core.k": {
        13,
        15,
        25,
        31,
        34,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        124,
        130,
        185,
        186,
        187,
        188,
    },
    "reference-semantics/semantics/call.k": {19},
    "reference-semantics/semantics/functions.k": {8, 9, 10, 11},
    "reference-semantics/semantics/methods.k": {10, 112, 115, 149, 162},
}

MODEL_DIVERGENCE = {
    ("reference-semantics/semantics/methods.k", 21),
    ("reference-semantics/semantics/methods.k", 113),
    ("reference-semantics/semantics/methods.k", 116),
    ("reference-semantics/semantics/methods.k", 150),
    ("reference-semantics/semantics/methods.k", 151),
    ("reference-semantics/semantics/methods.k", 152),
    ("reference-semantics/semantics/methods.k", 163),
    ("reference-semantics/semantics/methods.k", 164),
}


def entries(path: Path):
    lines = path.read_text().splitlines()
    starts = [
        (index + 1, START.match(line).group(1))
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    for position, (line_number, kind) in enumerate(starts):
        end = starts[position + 1][0] - 1 if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[line_number - 1 : end]).strip()
        yield line_number, kind, text


counts: Counter[tuple[str, str]] = Counter()
print(
    "id\tlocation\tkind\tattributes\trole_decision\tentry_sha256\tentry_preview"
)
identifier = 0
for path in FILES:
    relative = path.relative_to(SCRATCH).as_posix()
    for line_number, kind, text in entries(path):
        identifier += 1
        attributes = sorted(
            set(
                re.findall(
                    r"\b(functional|function|total|simplification|concrete|"
                    r"owise|macro|strict|seqstrict|priority|no-evaluators)\b",
                    text,
                )
            )
        )
        if kind == "rule":
            if (relative, line_number) in MODEL_DIVERGENCE:
                decision = "USED_FALSE_FOR_REAL_UNICODE_PYTHON"
            elif line_number in USED_RULES.get(relative, set()):
                decision = "USED_OK_ON_EXACT_EXECUTION_PATH"
            else:
                decision = "UNUSED_FIXED_BASELINE_NO_TARGET_INFLUENCE"
        elif kind == "claim":
            decision = "TARGET_RESULT_CONSTRAINING_CLAIM"
        elif line_number in USED_DECLARATIONS.get(relative, set()):
            decision = "USED_DECLARATION_OR_STRICTNESS"
        elif kind in {"syntax", "configuration", "context"}:
            decision = "UNUSED_OR_STRUCTURAL_DECLARATION"
        else:
            decision = "MODULE_STRUCTURE"
        counts[(kind, decision)] += 1
        preview = " ".join(text.split())
        if len(preview) > 600:
            preview = preview[:597] + "..."
        digest = hashlib.sha256(text.encode()).hexdigest()
        print(
            f"{identifier}\t{relative}:{line_number}\t{kind}\t"
            f"{','.join(attributes) or '-'}\t{decision}\t{digest}\t{preview}"
        )

print("SUMMARY")
print(f"files={len(FILES)}")
print(f"entries={identifier}")
for (kind, decision), count in sorted(counts.items()):
    print(f"{kind}\t{decision}\t{count}")
print("RULE_INVENTORY=COMPLETE")
