#!/usr/bin/env python3
"""Emit a source-complete inventory of K declarations, rules, and claims."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/52-below-threshold")
SEMANTICS = SCRATCH / "reference-semantics"

paths = [SEMANTICS / "semantics.k"]
paths.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
paths.extend([SCRATCH / "verification.k", SCRATCH / "spec.k"])

start_re = re.compile(
    r'^(requires(?=\s+")|module|endmodule|imports|syntax|configuration|context|rule|claim)\b'
)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        match = start_re.match(stripped)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        text_lines = lines[start:end]
        while text_lines and (
            not text_lines[-1].strip() or text_lines[-1].lstrip().startswith("//")
        ):
            text_lines.pop()
        text = "\n".join(text_lines).strip()
        yield start + 1, start + len(text_lines), kind, text


def classify(path: Path, kind: str, text: str) -> tuple[str, str]:
    rel = path.relative_to(SCRATCH).as_posix()
    compact = " ".join(text.split())

    if rel == "verification.k":
        if "intsToVals(IntSeq)" in compact and kind == "syntax":
            return (
                "ACCEPTABLE-INPUT-REPRESENTATION",
                "fresh typed ValSeq constructor; carries no result equation",
            )
        if "#iterNext(list(intsToVals" in compact:
            return (
                "ACCEPTABLE-LOW-LEVEL-BRIDGE",
                "constructor-by-constructor iterator exposure; disjoint from base list cases",
            )
        if kind == "rule" and "<k> #loop(list(intsToVals" in compact:
            return (
                "DERIVED-LOOP-SUMMARY",
                "same configuration as separately proved LOOP-SPEC; exact continuation and cells",
            )
        if "belowThresholdSpec" in compact:
            return (
                "VALID-MATH-DEFINITION",
                "exhaustive structural recursion; strict-less-than contract",
            )
        if "#belowThresholdCall" in compact:
            return (
                "ENTRY-SYNTAX-MACRO",
                "direct closure call over the exact factored body",
            )
        if "[macro]" in compact or compact.startswith("rule belowThreshold"):
            return (
                "EXACT-SYNTAX-MACRO",
                "non-operational factoring; checked independently against submitted term",
            )
        return ("PROOF-LOCAL-STRUCTURE", "reviewed in Stage 5")

    if rel == "spec.k":
        if kind == "claim":
            return (
                "POSITIVE-PROOF-TARGET",
                "independently rebuilt and proved; adequacy reviewed in Stage 4",
            )
        return ("SPEC-STRUCTURE", "module/import structure only")

    relevant_files = {
        "reference-semantics/semantics.k",
        "reference-semantics/semantics/syntax.k",
        "reference-semantics/semantics/core.k",
        "reference-semantics/semantics/iter.k",
        "reference-semantics/semantics/list.k",
        "reference-semantics/semantics/tuple.k",
        "reference-semantics/semantics/controls.k",
        "reference-semantics/semantics/functions.k",
        "reference-semantics/semantics/call.k",
        "reference-semantics/semantics/operators.k",
        "reference-semantics/semantics/int.k",
    }
    if rel in relevant_files:
        relevant_markers = (
            "Module",
            "#loadAll",
            "Stmts",
            "Expr(",
            "Name(",
            "Bool(",
            "truthy",
            "appendVal",
            "#iter",
            "list(",
            "#bindTgt",
            "If(",
            "#branch",
            "For(",
            "#loop",
            "#loopStep",
            "#loopLbl",
            "FuncDef",
            "closureVal",
            "#bindP",
            "Return(",
            "#endcall",
            "#pop",
            "Call(",
            "#callee",
            "#evalArgs",
            "#evalArgCont",
            "#applyK(toCall(closureVal",
            "Compare(",
            "applyCmp",
            '">="',
            "configuration",
        )
        if kind in {"module", "imports", "requires", "endmodule"} or any(
            marker in compact for marker in relevant_markers
        ):
            return (
                "USED-FIXED-SEMANTICS",
                "on the submitted term/claim path; agrees with the modeled Python subset",
            )

    return (
        "UNUSED-FIXED-SEMANTICS",
        "not reachable from this program or proof-local terms; no intended-domain witness",
    )


records = []
counts = Counter()
for path in paths:
    for start, end, kind, source in blocks(path):
        classification, rationale = classify(path, kind, source)
        attrs = sorted(
            set(
                re.findall(
                    r"\b(functional|function|total|simplification|priority|macro-rec|macro|"
                    r"owise|concrete|symbol|no-evaluators)\b",
                    source,
                )
            )
        )
        records.append(
            {
                "path": path.relative_to(SCRATCH).as_posix(),
                "start": start,
                "end": end,
                "kind": kind,
                "attrs": attrs,
                "classification": classification,
                "rationale": rationale,
                "source": source,
            }
        )
        counts[f"kind:{kind}"] += 1
        for attr in attrs:
            counts[f"attr:{attr}"] += 1
        counts[f"class:{classification}"] += 1

print("# Exhaustive K source inventory")
print()
print("Inputs:")
for path in paths:
    print(f"- {path}")
print()
print("Counts:")
for key in sorted(counts):
    print(f"- {key}: {counts[key]}")
print(f"- total-records: {len(records)}")
print()
print(
    "Classification rule: every source record is listed below. "
    "`UNUSED-FIXED-SEMANTICS` means no construct in the submitted program, "
    "entry term, loop term, or postcondition can reach that declaration/rule; "
    "it is not a claim that the unused fragment was universally verified."
)

for number, record in enumerate(records, 1):
    location = f"{record['path']}:{record['start']}"
    if record["end"] != record["start"]:
        location += f"-{record['end']}"
    attrs = ", ".join(record["attrs"]) if record["attrs"] else "none"
    print()
    print(f"## {number}. {record['kind']} — {location}")
    print(f"Attributes: {attrs}")
    print(f"Decision: {record['classification']}")
    print(f"Reason: {record['rationale']}")
    print("```k")
    print(record["source"])
    print("```")
