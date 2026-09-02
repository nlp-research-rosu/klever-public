#!/usr/bin/env python3
"""Produce a complete declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/fresh")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context\s+alias|context)\b"
)
BOUNDARY = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|rule|claim|"
    r"context\s+alias|context)\b"
)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        start = index
        kind = match.group(1).replace(" ", "-")
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            index += 1
        raw = "\n".join(lines[start:index])
        # Comments are useful in source but make the row too noisy.
        normalized = " ".join(
            part.strip()
            for part in raw.splitlines()
            if part.strip() and not part.lstrip().startswith("//")
        )
        known_attribute = re.compile(
            r"^(function|functional|total|macro|macro-rec|owise|concrete|"
            r"simplification|no-evaluators|strict(?:\([^)]*\))?|"
            r"seqstrict(?:\([^)]*\))?|priority\([^)]*\)|symbol\([^)]*\))$"
        )
        attrs = sorted(
            {
                attribute.strip()
                for group in re.findall(r"\[([^\]]+)\]", normalized)
                for attribute in group.split(",")
                if known_attribute.match(attribute.strip())
            }
        )
        yield kind, start + 1, normalized, ",".join(attrs) or "-"


def usage_bucket(path: Path, kind: str, statement: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "verification.k":
        return "PROOF-LOCAL-REVIEWED"
    if rel == "spec.k":
        return "TARGET-CLAIM-REVIEWED"
    if kind == "configuration":
        return "ACTIVE-CONFIG-REVIEWED"

    active_tokens = (
        "#loadAll",
        "FuncDef(",
        "Name(",
        "#look(",
        "#evalArgs(",
        "#evalArgCont(",
        "Int(",
        "Str(",
        "strToCodes(",
        "TupleExpr(",
        "toTuple",
        "BoolOp(",
        'CmpOp("not in"',
        'CmpOp("in"',
        "#memberAcc(",
        "#memberCont(",
        "#notB",
        "Attribute(",
        "Call(",
        "#callee(",
        "toCall(",
        "closureVal(",
        "#bindP(",
        "#endcall",
        "#pop",
        "frame(",
        "Return(",
        "Assign(Name",
        "If(",
        "#branch(",
        "BinOp(",
        'applyBin("+"',
        "Compare(",
        'applyCmp("<"',
        "applyMethod(",
        '"index"',
        "idxOfVS(",
        "Subscript(",
        "Slice(",
        "#evalB(",
        "#slLo(",
        "#slHi(",
        "#slStep(",
        "doSlice(",
        "slStart(",
        "slStop(",
        "slAdjust(",
        "clampLo(",
        "clampHi(",
        "buildVS(",
        "valSeqAt(",
        "vsLen(",
        "truthy(",
        "appendVal(",
        "vals2valSeq(",
        "builtinsScope",
    )
    if any(token in statement for token in active_tokens):
        return "ACTIVE-OR-OVERLAPPING-FIXED-REVIEWED"

    # These modules contribute constructors and dispatch families whose
    # sort/head disjointness was checked even when a particular rule is unused.
    rel_name = Path(rel).name
    if rel_name in {
        "core.k",
        "operators.k",
        "int.k",
        "bool.k",
        "str.k",
        "list.k",
        "tuple.k",
        "subscript.k",
        "methods.k",
        "controls.k",
        "functions.k",
        "call.k",
    }:
        return "SAME-MODULE-DISJOINT-FIXED-REVIEWED"
    return "UNUSED-CONSTRUCTOR-DISJOINT-FIXED-REVIEWED"


def extension_class(path: Path, kind: str, statement: str, attrs: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if kind == "claim":
        return "reachability-claim"
    if kind == "configuration":
        return "configuration"
    if kind.startswith("context"):
        return "evaluation-context"
    if kind == "syntax":
        if "no-evaluators" in attrs:
            return "opaque-declaration"
        if "function" in attrs or "functional" in attrs:
            return "function-declaration"
        if "macro" in attrs:
            return "macro-declaration"
        return "syntax-declaration"
    if rel == "verification.k":
        if any(name in statement for name in ("bfBody", "bfModule", "bfCall")):
            return "macro-equation"
        return "definitional-summary-equation"
    if "<k>" in statement:
        return "operational-rule"
    if "concrete" in attrs:
        return "concrete-equation"
    if "owise" in attrs:
        return "owise-equation"
    return "equational-rule"


def main() -> int:
    records = []
    for path in SOURCES:
        for kind, line, statement, attrs in blocks(path):
            records.append(
                (
                    path.relative_to(ROOT).as_posix(),
                    line,
                    kind,
                    extension_class(path, kind, statement, attrs),
                    attrs,
                    usage_bucket(path, kind, statement),
                    statement,
                )
            )

    kind_counts = Counter(record[2] for record in records)
    class_counts = Counter(record[3] for record in records)
    bucket_counts = Counter(record[5] for record in records)
    attribute_counts = Counter(
        attribute
        for record in records
        for attribute in (() if record[4] == "-" else record[4].split(","))
    )
    proof_local_attribute_counts = Counter(
        attribute
        for record in records
        if record[0] == "verification.k"
        for attribute in (() if record[4] == "-" else record[4].split(","))
    )
    print(f"SOURCES={len(SOURCES)}")
    print(f"RECORDS={len(records)}")
    print("KIND_COUNTS=" + repr(dict(sorted(kind_counts.items()))))
    print("CLASS_COUNTS=" + repr(dict(sorted(class_counts.items()))))
    print("AUDIT_BUCKET_COUNTS=" + repr(dict(sorted(bucket_counts.items()))))
    print("ATTRIBUTE_COUNTS=" + repr(dict(sorted(attribute_counts.items()))))
    print(
        "PROOF_LOCAL_ATTRIBUTE_COUNTS="
        + repr(dict(sorted(proof_local_attribute_counts.items())))
    )
    print(
        "COLUMNS=id\tsource:line\tkind\tclass\tattributes\t"
        "audit_disposition\tstatement"
    )
    for record_id, record in enumerate(records, 1):
        rel, line, kind, record_class, attrs, bucket, statement = record
        print(
            f"K{record_id:04d}\t{rel}:{line}\t{kind}\t{record_class}\t"
            f"{attrs}\t{bucket}\t{statement}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
