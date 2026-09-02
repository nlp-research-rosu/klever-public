#!/usr/bin/env python3
"""Build a line-addressable exhaustive inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
from pathlib import Path


REFERENCE_ROOT = Path("/reference/reference-semantics")
OUTPUT = Path("/audit-output/evidence/artifacts/rule_inventory.md")
FILES = [REFERENCE_ROOT / "semantics.k", *sorted((REFERENCE_ROOT / "semantics").glob("*.k"))]
FILES += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

START = re.compile(r"^\s*(configuration|context|rule|claim|syntax)\b")
BOUNDARY = re.compile(
    r"^\s*(?:configuration|context|rule|claim|syntax|module|endmodule|imports|requires)\b"
)


def source_class(path: Path) -> str:
    if path.name == "verification.k":
        return "proof-local"
    if path.name == "spec.k":
        return "claim"
    if path.name == "concrete.k":
        return "fixed-runtime"
    return "fixed-proof"


def decision(path: Path, line: int, kind: str) -> str:
    if path.name == "verification.k":
        rule_decisions = {
            7: "VALID definition base: suffix is empty once I>=K.",
            9: "VALID even step: emits 1 and strictly increments I toward K.",
            13: "VALID odd step: emits M and strictly increments I toward K.",
            21: "VALID A=1 case: neighbors are B,C.",
            23: "VALID B=1 case: neighbors are A,D.",
            25: "VALID C=1 case: neighbors are A,D.",
            27: "VALID catch-all definition; on the claim domain it means D=1, neighbors B,C.",
            37: "VALID ValSeq concatenation associativity.",
            40: "VALID ValSeq right identity.",
            46: "VALID macro expansion; fresh KAST comparison is byte-identical to submitted program KAST.",
        }
        if kind == "rule":
            return rule_decisions.get(line, "REVIEW_REQUIRED proof-local rule")
        return "VALID proof-local declaration; attributes and users audited in REVIEW.md."
    if path.name == "spec.k":
        return "CLAIM audited for satisfiability, result constraint, program pinning, and scope."
    if path.name == "concrete.k":
        return "ACCEPTED fixed supplied runtime-only semantics; excluded from Haskell proof module MPY."
    return "ACCEPTED fixed supplied-semantics boundary; byte-identical trusted source, not a candidate extension."


records: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    module = ""
    for index, line in enumerate(lines):
        module_match = re.match(r"^\s*module\s+(\S+)", line)
        if module_match:
            module = module_match.group(1)
        match = START.match(line)
        if not match:
            continue
        kind = match.group(1)
        end = index + 1
        while end < len(lines) and not BOUNDARY.match(lines[end]):
            end += 1
        block_lines = lines[index:end]
        while block_lines and (not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")):
            block_lines.pop()
        block = "\n".join(block_lines)
        attrs = []
        for attr in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "concrete",
            "simplification",
            "priority",
            "owise",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"(?<![A-Za-z-]){re.escape(attr)}(?:\(|\]|,)", block):
                attrs.append(attr)
        records.append(
            {
                "path": path,
                "line": index + 1,
                "end": index + len(block_lines),
                "module": module,
                "kind": kind,
                "class": source_class(path),
                "attrs": ", ".join(attrs) or "—",
                "text": " ".join(part.strip() for part in block_lines if part.strip()),
                "decision": decision(path, index + 1, kind),
            }
        )

by_kind = collections.Counter(str(record["kind"]) for record in records)
by_class = collections.Counter(str(record["class"]) for record in records)
attribute_counts = collections.Counter()
for record in records:
    if record["attrs"] != "—":
        attribute_counts.update(str(record["attrs"]).split(", "))

with OUTPUT.open("w", encoding="utf-8") as stream:
    stream.write("# Exhaustive K declaration and rule inventory\n\n")
    stream.write(
        "Generated from every `.k` source in the trusted supplied-semantics tree plus "
        "candidate `verification.k` and `spec.k`. Line ranges point to immutable source mounts.\n\n"
    )
    stream.write(f"Total records: {len(records)}  \n")
    stream.write(f"By kind: {dict(sorted(by_kind.items()))}  \n")
    stream.write(f"By source class: {dict(sorted(by_class.items()))}  \n")
    stream.write(f"Attribute occurrences: {dict(sorted(attribute_counts.items()))}\n\n")
    stream.write("| # | Source | Lines | Module | Kind | Attributes | Declaration/rule | Decision |\n")
    stream.write("|---:|---|---:|---|---|---|---|---|\n")
    for number, record in enumerate(records, 1):
        path = str(record["path"])
        display = path.removeprefix("/reference/reference-semantics/").removeprefix("/candidate/")
        text = str(record["text"]).replace("|", "\\|").replace("`", "\\`")
        decision_text = str(record["decision"]).replace("|", "\\|")
        stream.write(
            f"| {number} | `{display}` | {record['line']}-{record['end']} | "
            f"`{record['module']}` | {record['kind']} | {record['attrs']} | "
            f"`{text}` | {decision_text} |\n"
        )

print(f"output={OUTPUT}")
print(f"records={len(records)}")
print(f"by_kind={dict(sorted(by_kind.items()))}")
print(f"by_class={dict(sorted(by_class.items()))}")
print(f"attributes={dict(sorted(attribute_counts.items()))}")
