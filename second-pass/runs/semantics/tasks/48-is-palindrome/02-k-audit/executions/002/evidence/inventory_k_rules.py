#!/usr/bin/env python3
"""Create a source-derived inventory of K declarations and rule attributes."""

from __future__ import annotations

import argparse
import collections
import pathlib
import re


START = re.compile(r"^(syntax|rule|claim|context|configuration|alias)\b")
ATTRIBUTE_NAMES = (
    "function",
    "total",
    "functional",
    "simplification",
    "owise",
    "priority",
    "macro",
    "macro-rec",
    "symbol",
    "concrete",
)
TARGET_TERMS = (
    "#loadAll",
    "Module",
    "FuncDef",
    "Params",
    "Return",
    "Call",
    "#callee",
    "#evalArgs",
    "#evalArgCont",
    "toCall",
    "#applyK",
    "closureVal",
    "#bindP",
    "#endcall",
    "#pop",
    "Name",
    "#look",
    "Compare",
    "CmpOp",
    "applyCmp",
    "UnaryOp",
    'applyUn("-"',
    "Subscript",
    "Slice",
    "Bound",
    "#evalB",
    "#slLo",
    "#slHi",
    "#slStep",
    "doSlice",
    "slStep",
    "slStart",
    "slStop",
    "slAdjust",
    "clampLo",
    "clampHi",
    "buildIS",
    "intSeqAt",
    "isLen",
    "str(",
    "palindrome",
)


def declarations(path: pathlib.Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    output: list[tuple[int, str, str]] = []
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        match = START.match(stripped)
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        block = [stripped]
        index += 1
        while index < len(lines):
            continuation = lines[index].strip()
            if not continuation:
                break
            if START.match(continuation):
                break
            if continuation.startswith(
                ("module ", "endmodule", "imports ", "requires ", "//")
            ):
                break
            block.append(continuation)
            index += 1
        output.append((start + 1, kind, " ".join(block)))
    return output


parser = argparse.ArgumentParser()
parser.add_argument("--root", type=pathlib.Path, required=True)
parser.add_argument("--extra", type=pathlib.Path, action="append", default=[])
parser.add_argument("--out", type=pathlib.Path, required=True)
args = parser.parse_args()

paths = sorted(args.root.rglob("*.k")) + args.extra
rows: list[tuple[str, int, str, str, str, str, str]] = []
counts: collections.Counter[str] = collections.Counter()
attribute_counts: collections.Counter[str] = collections.Counter()

for path in paths:
    source_label = str(path)
    for line, kind, text in declarations(path):
        present_attrs = [
            name
            for name in ATTRIBUTE_NAMES
            if re.search(rf"(?<![A-Za-z-]){re.escape(name)}(?![A-Za-z-])", text)
        ]
        attrs = ",".join(present_attrs)
        attribute_counts.update(present_attrs)
        classification = kind
        if kind == "rule":
            if "simplification" in attrs:
                classification = "simplification-rule"
            elif "macro" in attrs:
                classification = "macro-rule"
            elif "owise" in attrs:
                classification = "owise-rule"
            else:
                classification = "ordinary-rule"
        elif kind == "syntax" and "function" in attrs:
            classification = "function-syntax"
        is_candidate_extension = path.name == "verification.k"
        is_target_claim = path.name == "spec.k"
        target_relevant = is_candidate_extension or is_target_claim or any(
            term in text for term in TARGET_TERMS
        )
        if is_candidate_extension:
            decision = "ACCEPT_TRUTHFUL_DEFINITION_NO_EXECUTION_REPLACEMENT"
        elif is_target_claim:
            decision = "TARGET_CLAIM_NOT_AN_AXIOM"
        elif "no-evaluators" in text or "symbol(" in text:
            decision = "ACCEPT_FIXED_TRUST_BOUNDARY_UNUSED_BY_TARGET"
        elif target_relevant:
            decision = "ACCEPT_FIXED_FAITHFUL_ON_TARGET_PATH"
        else:
            decision = "ACCEPT_FIXED_UNUSED_BY_TARGET"
        rows.append(
            (
                source_label,
                line,
                kind,
                classification,
                attrs,
                "target" if target_relevant else "unused",
                decision,
                text,
            )
        )
        counts[classification] += 1

with args.out.open("w", encoding="utf-8") as stream:
    stream.write(
        "file\tline\tkind\tclassification\tattributes\trelevance\tdecision\tdeclaration\n"
    )
    for row in rows:
        stream.write("\t".join(str(field).replace("\t", " ") for field in row) + "\n")

print(f"FILES={len(paths)}")
print(f"DECLARATIONS={len(rows)}")
for key in sorted(counts):
    print(f"{key}={counts[key]}")
for key in sorted(attribute_counts):
    print(f"attribute_{key}={attribute_counts[key]}")
print(f"INVENTORY={args.out}")
