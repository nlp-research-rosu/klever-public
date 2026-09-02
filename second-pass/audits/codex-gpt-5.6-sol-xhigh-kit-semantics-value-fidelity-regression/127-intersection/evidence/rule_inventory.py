#!/usr/bin/env python3
"""Emit a complete declaration/rule/claim inventory with audit disposition."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/127-intersection")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(r"^\s*(syntax|rule|claim|context|configuration)\b")
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|claim|context|configuration|module|endmodule|imports|requires)\b"
)

# Starts of declarations/rules exercised by the submitted program's entry
# claim. Syntax declarations in syntax.k are separately mapped by
# used-construct-map.md.
USED_STARTS = {
    "reference-semantics/semantics/core.k": {
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        124,
        126,
        127,
        130,
        131,
        132,
        185,
        186,
        189,
        190,
        191,
        194,
        199,
        202,
        208,
        209,
        210,
        213,
        214,
        215,
        217,
        218,
        219,
        223,
        224,
        225,
    },
    "reference-semantics/semantics/call.k": {19, 20, 21, 69},
    "reference-semantics/semantics/controls.k": {
        9,
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
    "reference-semantics/semantics/functions.k": {
        8,
        63,
        64,
        78,
        85,
    },
    "reference-semantics/semantics/int.k": {
        9,
        13,
        14,
        15,
        19,
        20,
        22,
        24,
        26,
    },
    "reference-semantics/semantics/operators.k": {12, 15, 16, 17},
    "reference-semantics/semantics/str.k": {13, 14, 15, 16},
    "reference-semantics/semantics/subscript.k": {
        11,
        12,
        13,
        16,
        17,
        18,
        21,
        22,
        23,
        27,
        28,
        35,
        37,
        39,
    },
    "reference-semantics/semantics/tuple.k": {14, 15, 16},
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def flatten(lines: list[str]) -> str:
    text = " ".join(piece.strip() for piece in lines)
    text = re.sub(r"\s+", " ", text).strip()
    return text.replace("\t", " ")


rows = []
counts = Counter()
counts["attr:functional"] = 0
counts["attr:simplification"] = 0
counts["category:simplification-rule"] = 0
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for i in starts:
        match = START.match(lines[i])
        assert match is not None
        kind = match.group(1)
        j = i + 1
        while j < len(lines) and not BOUNDARY.match(lines[j]):
            j += 1
        block = flatten(lines[i:j])
        attrs = []
        for attr in (
            "function",
            "total",
            "functional",
            "simplification",
            "priority",
            "concrete",
            "owise",
            "macro",
            "macro-rec",
            "no-evaluators",
            "symbol",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", block):
                attrs.append(attr)

        relative = rel(path)
        line_no = i + 1
        if relative == "verification.k":
            disposition = "PROOF_LOCAL_REVIEWED_SOUND"
        elif relative == "spec.k":
            disposition = "CLAIM_REVIEWED_RESULT_CONSTRAINING"
        elif relative.endswith("/syntax.k"):
            disposition = "SUPPLIED_SYNTAX_SEE_CONSTRUCT_MAP"
        elif line_no in USED_STARTS.get(relative, set()):
            disposition = "SUPPLIED_USED_PATH_REVIEWED_SOUND"
        else:
            disposition = "SUPPLIED_FIXED_UNUSED_BY_ENTRY_PROOF"

        if kind == "rule":
            category = (
                "simplification-rule"
                if "simplification" in attrs
                else "ordinary-rule"
            )
        elif kind == "syntax":
            if "no-evaluators" in attrs or "symbol" in attrs:
                category = "opaque-symbol-declaration"
            elif "function" in attrs:
                category = "function-declaration"
            else:
                category = "syntax-declaration"
        else:
            category = kind
        counts[f"kind:{kind}"] += 1
        counts[f"category:{category}"] += 1
        for attr in attrs:
            counts[f"attr:{attr}"] += 1
        rows.append(
            (
                len(rows) + 1,
                relative,
                line_no,
                kind,
                category,
                ",".join(attrs) or "-",
                disposition,
                block,
            )
        )

print(
    "index\tfile\tline\tkind\tcategory\tattributes\tdisposition\tdeclaration"
)
for row in rows:
    print("\t".join(str(value) for value in row))
print("# SUMMARY")
print(f"# files={len(FILES)}")
print(f"# inventory_items={len(rows)}")
for key in sorted(counts):
    print(f"# {key}={counts[key]}")
