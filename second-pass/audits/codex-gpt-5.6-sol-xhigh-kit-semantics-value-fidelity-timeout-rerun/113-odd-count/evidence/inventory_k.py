#!/usr/bin/env python3
"""Lexically inventory every K declaration, context, rule, and claim in scope.

The normalized source text and exact location remain in JSONL so multiline
rules are not truncated. Assessment labels are reviewer-authored classifications
whose rationale is documented in REVIEW.md.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


SOURCE = Path("/tmp/audit-work/source")
EVIDENCE = Path("/audit-output/evidence")

paths = [SOURCE / "reference-semantics" / "semantics.k"]
paths.extend(sorted((SOURCE / "reference-semantics" / "semantics").glob("*.k")))
paths.extend([SOURCE / "verification.k", SOURCE / "spec.k"])

start_re = re.compile(r"^\s*(syntax|context|configuration|rule|claim)\b")
terminal_re = re.compile(r"^(?:requires|module)\b|^\s{0,2}(?:endmodule|imports)\b")

used_markers = {
    "#alloc",
    "#applyK",
    "#bindP",
    "#callee",
    "#endcall",
    "#evalArg",
    "#evalArgs",
    "#iterDone",
    "#iterNext",
    "#iterYield",
    "#loadAll",
    "#look",
    "#loop",
    "#loopStep",
    "#pop",
    "applyBin",
    "applyBuiltin",
    "applyMethod",
    "appendVal",
    "Attribute(",
    "BinOp(",
    "Call(",
    "closureVal",
    "Expr(",
    "For(",
    "FuncDef(",
    "iCons",
    "isMutMethod",
    "ListExpr(",
    "Name(",
    "Return(",
    "seqConcat",
    "Str(",
    "strToCodes",
    "valSeqConcat",
    "vCons",
}

candidate_rule_assessment = {
    10: (
        "ACCEPT_EXACT_PROGRAM_MACRO",
        "Compile-time abbreviation; fresh depth-zero expansion matches solution.mpy.",
    ),
    16: (
        "ACCEPT_EXACT_PROGRAM_MACRO",
        "Compile-time loop-body abbreviation; included in exact expansion comparison.",
    ),
    72: (
        "ACCEPT_TRUE_DEFINITION",
        "Empty ValSeq contains only strings.",
    ),
    73: (
        "ACCEPT_TRUE_DEFINITION",
        "Constructor recursion exactly conjoins head string-ness with the tail.",
    ),
    78: (
        "ACCEPT_USED_DOMAIN_WITH_TOTALITY_CONCERN",
        "True string-constructor projection on every use; [total] is broader than its sole equation.",
    ),
    85: (
        "ACCEPT_GROUND_EXHAUSTIVE_PRIMITIVE_EQUATION",
        "For every ground code sequence and code, expands to supplied cntSub on the one-code pattern.",
    ),
    92: (
        "ACCEPT_OPERATIONAL_BRIDGE",
        "After receiver/argument evaluation, matches one-character str.count and equals the supplied rule on ground strings.",
    ),
    102: (
        "ACCEPT_TRUE_DEFINITION",
        "Sums counts of ASCII digit codes 1,3,5,7,9.",
    ),
    113: (
        "ACCEPT_GROUND_EXHAUSTIVE_PRIMITIVE_EQUATION",
        "For every ground integer, expands to the exact supplied Int2String/strToCodes expression.",
    ),
    114: (
        "ACCEPT_OPERATIONAL_BRIDGE",
        "After ordinary builtin resolution/evaluation, equals the supplied str(Int) result on ground integers.",
    ),
    118: (
        "ACCEPT_TRUE_DEFINITION",
        "Left-associated code concatenation exactly mirrors the source output expression.",
    ),
    138: (
        "ACCEPT_TRUE_DEFINITION",
        "Wraps the defined sentence code sequence as a modeled string.",
    ),
    143: (
        "ACCEPT_TRUE_DEFINITION",
        "Empty remaining input preserves the accumulator.",
    ),
    144: (
        "ACCEPT_TRUE_GUARDED_RECURSION",
        "String-head step appends one sentence and strictly consumes the tail.",
    ),
    153: (
        "ACCEPT_TRUE_DEFINITION",
        "The initial result list sequence is empty.",
    ),
}

candidate_claim_assessment = {
    8: (
        "ACCEPT_DERIVED_LOOP_CIRCULARITY",
        "Matches the actual #loop state and summarizes one real body iteration.",
    ),
    47: (
        "ACCEPT_RESULT_CONSTRAINING_ENTRY",
        "Loads/calls the exact body and fixes returned ref, heap result, normal control, and allocation.",
    ),
}


def normalize(block: list[str]) -> str:
    return " ".join(" ".join(block).split())


def flags(text: str) -> list[str]:
    result = []
    checks = [
        ("function", r"\bfunction\b"),
        ("functional", r"\bfunctional\b"),
        ("total", r"\btotal\b"),
        ("symbol", r"\bsymbol(?:\([^]]*\))?"),
        ("no-evaluators", r"\bno-evaluators\b"),
        ("priority", r"\bpriority\("),
        ("simplification", r"\bsimplification\b"),
        ("concrete", r"\bconcrete\b"),
        ("owise", r"\bowise\b"),
        ("macro", r"\bmacro(?:-rec)?\b"),
        ("cell-rule", r"<[A-Za-z][^>]*>"),
    ]
    for name, pattern in checks:
        if re.search(pattern, text):
            result.append(name)
    return result


def assessment(path: Path, kind: str, line: int, text: str):
    if path.name == "verification.k":
        if kind == "rule":
            return candidate_rule_assessment.get(
                line,
                (
                    "REVIEW_ERROR_UNCLASSIFIED_CANDIDATE_RULE",
                    "Candidate rule was not in the expected reviewed line map.",
                ),
            )
        if kind == "syntax":
            if "oddBody" in text or "oddLoopBody" in text:
                return (
                    "ACCEPT_EXACT_PROGRAM_MACRO_DECLARATION",
                    "Macro declarations for freshly identity-checked AST subtrees.",
                )
            if "digitOccurrences" in text or "intStringCodes" in text:
                return (
                    "ACCEPT_OPAQUE_GROUND_DEFINED_PRIMITIVE_DECLARATION",
                    "Opaque symbol has an exhaustive ground concrete equation; symbolic proof remains parametric.",
                )
            if "codesProj" in text:
                return (
                    "CONCERN_OVERBROAD_TOTAL_DECLARATION",
                    "Only the string case is equated although the input sort is Val; theorem uses are guarded.",
                )
            return (
                "ACCEPT_DEFINITIONAL_DECLARATION",
                "Pure proof-summary declaration with reviewed equations.",
            )
    if path.name == "spec.k" and kind == "claim":
        return candidate_claim_assessment.get(
            line,
            (
                "REVIEW_ERROR_UNCLASSIFIED_CLAIM",
                "Claim was not in the expected reviewed line map.",
            ),
        )
    if "reference-semantics" in path.parts:
        used = any(marker in text for marker in used_markers)
        if used:
            return (
                "ACCEPT_SELECTED_SEMANTICS_USED_PATH",
                "Trusted supplied-semantics rule/declaration; also inspected on the submitted program's reachable path.",
            )
        return (
            "ACCEPT_SELECTED_SEMANTICS_OUT_OF_PATH",
            "Unmodified trusted supplied-semantics rule/declaration, unreachable from solution.mpy on the formal precondition.",
        )
    return ("ACCEPT_AUXILIARY", "Reviewer inventory auxiliary item.")


records = []
for path in paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        for stop in range(index + 1, end):
            if terminal_re.match(lines[stop]):
                end = stop
                break
        block = lines[index:end]
        while block and not block[-1].strip():
            block.pop()
        text = normalize(block)
        semantic_text = normalize(
            [re.sub(r"//.*$", "", line) for line in block]
        )
        item_flags = flags(semantic_text)
        decision, rationale = assessment(path, kind, index + 1, text)
        records.append(
            {
                "id": len(records) + 1,
                "source_kind": (
                    "supplied-semantics"
                    if "reference-semantics" in path.parts
                    else "candidate"
                ),
                "file": str(path),
                "line": index + 1,
                "kind": kind,
                "flags": item_flags,
                "assessment": decision,
                "rationale": rationale,
                "text": text,
            }
        )

inventory_path = EVIDENCE / "k-inventory.jsonl"
with inventory_path.open("w", encoding="utf-8") as output:
    for record in records:
        output.write(json.dumps(record, sort_keys=True) + "\n")

by_kind = Counter(record["kind"] for record in records)
by_assessment = Counter(record["assessment"] for record in records)
by_flag = Counter(flag for record in records for flag in record["flags"])
by_file = defaultdict(Counter)
for record in records:
    by_file[record["file"]][record["kind"]] += 1

summary = [
    "# Exhaustive K inventory summary",
    "",
    f"Records: {len(records)}",
    "",
    "## Source hashes",
    "",
]
for path in paths:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    summary.append(f"- `{path}`: `{digest}`")
summary.extend(["", "## Counts by kind", ""])
for kind, count in sorted(by_kind.items()):
    summary.append(f"- {kind}: {count}")
summary.extend(["", "## Counts by assessment", ""])
for decision, count in sorted(by_assessment.items()):
    summary.append(f"- {decision}: {count}")
summary.extend(["", "## Counts by attribute/shape flag", ""])
for flag, count in sorted(by_flag.items()):
    summary.append(f"- {flag}: {count}")
summary.extend(["", "## Counts by file", ""])
for file, counts in sorted(by_file.items()):
    rendered = ", ".join(f"{kind}={count}" for kind, count in sorted(counts.items()))
    summary.append(f"- `{file}`: {rendered}")
summary.extend(
    [
        "",
        "Every full normalized item, location, attributes, assessment, and rationale",
        "is in `k-inventory.jsonl`.",
        "",
    ]
)
(EVIDENCE / "k-inventory-summary.md").write_text(
    "\n".join(summary), encoding="utf-8"
)

print(f"inventory={inventory_path}")
print(f"records={len(records)}")
for kind, count in sorted(by_kind.items()):
    print(f"kind_{kind}={count}")
for decision, count in sorted(by_assessment.items()):
    print(f"assessment_{decision}={count}")
for flag, count in sorted(by_flag.items()):
    print(f"flag_{flag}={count}")
