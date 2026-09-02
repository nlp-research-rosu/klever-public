#!/usr/bin/env python3
"""Emit a complete declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from pathlib import Path


ROOTS = [
    (Path("/reference/reference-semantics"), "SUPPLIED"),
    (Path("/candidate/verification.k"), "PROOF_LOCAL"),
    (Path("/candidate/spec.k"), "SPEC"),
]
START = re.compile(r"^\s*(configuration|context|syntax|rule|claim)\b")
BOUNDARY = re.compile(
    r"^\s*(configuration|context|syntax|rule|claim|module|endmodule|imports)\b"
)
ATTRIBUTE = re.compile(r"\[([^\]]+)\]")


def sources():
    for root, origin in ROOTS:
        if root.is_dir():
            for path in sorted(root.rglob("*.k")):
                yield path, origin
        else:
            yield root, origin


records: list[dict[str, str | int]] = []
for path, origin in sources():
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for start in starts:
        end = start + 1
        while end < len(lines) and not BOUNDARY.match(lines[end]):
            end += 1
        text = " ".join(part.strip() for part in lines[start:end] if part.strip())
        match = START.match(lines[start])
        assert match is not None
        kind = match.group(1)
        attrs = ",".join(ATTRIBUTE.findall(text))
        if kind == "syntax":
            if "no-evaluators" in text or "symbol(" in text and "[concrete]" not in text:
                category = "OPAQUE_OR_SYMBOL_DECL"
            elif "function" in text or "functional" in text:
                category = "FUNCTION_DECL"
            else:
                category = "SYNTAX_DECL"
        elif kind == "rule":
            if "simplification" in attrs:
                category = "SIMPLIFICATION_RULE"
            elif "<k>" in text or any(
                cell in text
                for cell in (
                    "<env>",
                    "<scopes>",
                    "<heap>",
                    "<stack>",
                    "<ret>",
                    "<exc>",
                    "<exit-code>",
                )
            ):
                category = "OPERATIONAL_RULE"
            else:
                category = "EQUATIONAL_OR_MACRO_RULE"
        elif kind == "claim":
            category = "REACHABILITY_CLAIM"
        else:
            category = kind.upper()
        if origin == "SUPPLIED":
            decision = "ACCEPTED_SUPPLIED_BASELINE"
            rel = path.relative_to(Path("/reference/reference-semantics")).as_posix()
        elif origin == "PROOF_LOCAL":
            decision = "MANUAL_PROOF_EXTENSION_REVIEW"
            rel = "verification.k"
        else:
            decision = "MANUAL_CLAIM_REVIEW"
            rel = "spec.k"
        records.append(
            {
                "origin": origin,
                "file": rel,
                "start": start + 1,
                "end": end,
                "kind": kind,
                "category": category,
                "attrs": attrs or "-",
                "decision": decision,
                "text": text.replace("\t", " "),
            }
        )

print(
    "origin\tfile\tlines\tkind\tcategory\tattributes\tdecision\tdeclaration"
)
for record in records:
    print(
        "{origin}\t{file}\t{start}-{end}\t{kind}\t{category}\t{attrs}\t"
        "{decision}\t{text}".format(**record)
    )

from collections import Counter

print("\nCOUNTS")
print("total", len(records))
for key, value in sorted(Counter(r["origin"] for r in records).items()):
    print("origin", key, value)
for key, value in sorted(Counter(r["category"] for r in records).items()):
    print("category", key, value)
print(
    "priority_records",
    sum("priority" in str(r["attrs"]) for r in records),
)
print(
    "total_declarations",
    sum("total" in str(r["attrs"]) for r in records),
)
print(
    "functional_declarations",
    sum("functional" in str(r["attrs"]) for r in records),
)
print(
    "simplification_rules",
    sum(r["category"] == "SIMPLIFICATION_RULE" for r in records),
)
print(
    "opaque_or_symbol_declarations",
    sum(r["category"] == "OPAQUE_OR_SYMBOL_DECL" for r in records),
)
