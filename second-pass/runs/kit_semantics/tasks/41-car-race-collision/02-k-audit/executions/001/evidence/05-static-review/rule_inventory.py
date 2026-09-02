#!/usr/bin/env python3
"""Exhaustive source-sentence inventory with target-path classification."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


SEMANTICS_ROOT = Path("/tmp/audit-work/candidate-src/reference-semantics")
CANDIDATE_ROOT = Path("/tmp/audit-work/candidate-src")
OUTPUT = Path("/audit-output/evidence/05-static-review/rule_inventory.tsv")
SUMMARY = Path("/audit-output/evidence/05-static-review/summary.txt")

sources = [SEMANTICS_ROOT / "semantics.k"]
sources.extend(sorted((SEMANTICS_ROOT / "semantics").glob("*.k")))
sources.extend([CANDIDATE_ROOT / "verification.k", CANDIDATE_ROOT / "spec.k"])

sentence_start = re.compile(
    r'^(requires)(?=\s+")|^\s*(module|imports|syntax|configuration|rule|context|claim|endmodule)\b'
)
interesting = {"syntax", "configuration", "rule", "context", "claim"}
attribute_names = [
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "no-evaluators",
    "symbol",
]


target_fragments = {
    "semantics/syntax.k": [
        'syntax Expr ::= "Int"',
        '| "Name"',
        '| "BinOp"',
        '| "Call"',
        'syntax Stmt ::= "Assign"',
        '| "Return"',
        '| "FuncDef"',
        "syntax Stmts",
        "syntax Params",
        "syntax ParamNames",
        "syntax Module",
    ],
    "semantics/core.k": [
        "syntax Val      ::= Int",
        "syntax KResult",
        "syntax Expr     ::= Val",
        "syntax Vals",
        "syntax RetState",
        "configuration",
        "syntax KItem ::= #loadAll",
        "rule <k> #loadAll",
        "rule <k> (S:Stmt SS:Stmts)",
        "rule <k> .Stmts",
        "syntax KItem ::= #look",
        "rule <k> Name(",
        "rule <k> #look(X:String, L:Int) => {M[X]}",
        'syntax Scope ::= "builtinsScope"',
        "rule builtinsScope",
        "syntax ApplyK ::= toCall",
        "syntax KItem  ::= #evalArgs",
        "rule <k> #evalArgs((A:Expr",
        "rule <k> V:Val ~> #evalArgCont",
        "rule <k> #evalArgs(.Exprs",
        "rule <k> Int(I:Int)",
        "syntax Val  ::= applyUn",
        "syntax Val  ::= applyBin",
        "syntax Vals ::= appendVal",
        "rule appendVal(",
    ],
    "semantics/operators.k": [
        "rule <k> BinOp(",
    ],
    "semantics/int.k": [
        'rule applyBin("*"',
    ],
    "semantics/functions.k": [
        "syntax KItem ::= frame(",
        "rule <k> FuncDef(",
        "rule <k> #bindP(.ParamNames",
        "rule <k> #bindP((P:String",
        "rule <k> Return(V:Val)",
        "rule <k> #pop",
    ],
    "semantics/call.k": [
        "syntax KItem ::= #callee",
        "rule <k> Call(Fe:Expr",
        "rule <k> CV:Val ~> #callee",
        "rule <k> #applyK(toCall(closureVal(",
    ],
    "spec.k": [
        "claim [car-race-collision]",
    ],
}


def relative_name(path: Path) -> str:
    if path.is_relative_to(SEMANTICS_ROOT):
        return path.relative_to(SEMANTICS_ROOT).as_posix()
    return path.name


def parse(path: Path):
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = sentence_start.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    starts.append((len(lines), "EOF"))
    for position, (start, kind) in enumerate(starts[:-1]):
        end = starts[position + 1][0]
        text_lines = lines[start:end]
        while text_lines and (
            not text_lines[-1].strip()
            or text_lines[-1].lstrip().startswith("//")
        ):
            text_lines.pop()
        text = "\n".join(text_lines)
        yield start + 1, kind, text


rows = []
identifier = 0
for source in sources:
    rel = relative_name(source)
    for line, kind, text in parse(source):
        identifier += 1
        compact = " ".join(part.strip() for part in text.splitlines())
        attribute_text = " ".join(re.findall(r"\[([^\]]*)\]", text))
        attrs = [
            name
            for name in attribute_names
            if re.search(rf"\b{re.escape(name)}\b", attribute_text)
        ]
        target_path = any(
            fragment in text for fragment in target_fragments.get(rel, [])
        )
        if rel == "semantics/functions.k" and (
            "CellVars" in text or "#cellW" in text
        ):
            target_path = False
        if rel == "semantics/operators.k" and "ref(" in text:
            target_path = False
        if rel == "verification.k" and kind in interesting:
            review = "PROOF_LOCAL_REVIEW_REQUIRED"
        elif rel == "spec.k" and kind == "claim":
            review = "TARGET_OBLIGATION_RESULT_CONSTRAINING"
        elif "no-evaluators" in attrs:
            review = "ACCEPTED_UNUSED_OPAQUE_FIXED_BOUNDARY"
        elif "concrete" in attrs:
            review = "ACCEPTED_UNUSED_CONCRETE_FIXED_RULE"
        elif target_path:
            review = "ACCEPTED_TARGET_PATH_SOUND"
        elif kind in interesting:
            review = "ACCEPTED_OFF_PATH_FIXED_SUBSET"
        else:
            review = "STRUCTURE_ONLY"
        rows.append(
            {
                "id": f"S{identifier:04d}",
                "file": rel,
                "line": line,
                "kind": kind,
                "attributes": ",".join(attrs),
                "target_path": "yes" if target_path else "no",
                "review_decision": review,
                "text": compact,
            }
        )

with OUTPUT.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "id",
            "file",
            "line",
            "kind",
            "attributes",
            "target_path",
            "review_decision",
            "text",
        ],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)

kind_counts = Counter(row["kind"] for row in rows)
attribute_counts = Counter(
    attr
    for row in rows
    for attr in row["attributes"].split(",")
    if attr
)
review_counts = Counter(row["review_decision"] for row in rows)
file_rule_counts = Counter(
    row["file"] for row in rows if row["kind"] == "rule"
)

with SUMMARY.open("w") as stream:
    print("sources:", len(sources), file=stream)
    print("sentences:", len(rows), file=stream)
    print("kinds:", dict(sorted(kind_counts.items())), file=stream)
    print(
        "attributes:", dict(sorted(attribute_counts.items())), file=stream
    )
    print("review_decisions:", dict(sorted(review_counts.items())), file=stream)
    print("rules_by_file:", file=stream)
    for file, count in sorted(file_rule_counts.items()):
        print(f"  {file}: {count}", file=stream)
    print(
        "verification_local_interesting_sentences:",
        sum(
            row["file"] == "verification.k"
            and row["kind"] in interesting
            for row in rows
        ),
        file=stream,
    )
    print(
        "proof_local_rule_count:",
        sum(
            row["file"] == "verification.k" and row["kind"] == "rule"
            for row in rows
        ),
        file=stream,
    )
    print(
        "simplification_count:",
        attribute_counts["simplification"],
        file=stream,
    )
    print(
        "functional_attribute_count:",
        attribute_counts["functional"],
        file=stream,
    )
    print(
        "opaque_no_evaluators_count:",
        attribute_counts["no-evaluators"],
        file=stream,
    )
    print("INVENTORY: COMPLETE", file=stream)

print(SUMMARY.read_text(), end="")
