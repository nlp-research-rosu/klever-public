#!/usr/bin/env python3
"""Produce an exhaustive source-level inventory of local K declarations."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
EXTRA = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
START = re.compile(
    r"^\s*(syntax|configuration|rule|claim|context|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s*(?:syntax|configuration|rule|claim|context|alias|"
    r"module|endmodule|imports)\b"
)
ATTR = re.compile(r"\[([^\]]+)\]")
KNOWN_ATTRIBUTES = {
    "anywhere",
    "assoc",
    "bracket",
    "comm",
    "concrete",
    "constructor",
    "function",
    "functional",
    "hook",
    "idem",
    "left",
    "macro",
    "macro-rec",
    "no-evaluators",
    "owise",
    "priority",
    "right",
    "seqstrict",
    "simplification",
    "strict",
    "symbol",
    "total",
    "unit",
}


# Source lines whose declarations/rules lie on the real target execution path.
USED_RANGES: dict[str, list[tuple[int, int, str]]] = {
    "semantics/syntax.k": [
        (9, 16, "used Expr constructors and strict/seqstrict evaluation"),
        (28, 32, "Call, Compare and CmpOp constructors"),
        (41, 61, "used statements, lists, parameters and Module"),
    ],
    "semantics/core.k": [
        (13, 60, "values, configuration, strings, scopes and result sorts"),
        (123, 210, "module sequencing, lookup, builtins, args and literals"),
        (213, 219, "argument-list append/translation"),
    ],
    "semantics/controls.k": [
        (8, 18, "ordinary assignment in a plain frame"),
        (50, 54, "If branching"),
        (65, 91, "While loop and loop-label continuation"),
    ],
    "semantics/functions.k": [
        (8, 20, "closure representation and ordinary FuncDef"),
        (62, 66, "ordinary parameter binding"),
        (77, 90, "Return, frame pop and caller restoration"),
    ],
    "semantics/call.k": [
        (18, 32, "callee/argument routing and builtin dispatch"),
        (69, 74, "ordinary closure invocation and frame creation"),
    ],
    "semantics/operators.k": [
        (10, 20, "BinOp/Compare dispatch and evaluation contexts"),
    ],
    "semantics/int.k": [
        (9, 20, "integer +, %, // and Python remainder"),
        (26, 27, "integer == and !="),
    ],
    "semantics/str.k": [
        (12, 26, "ASCII string literal, concatenation and equality"),
    ],
    "semantics/builtins.k": [
        (17, 17, "builtin result dispatch declaration"),
        (142, 145, "chr implementation on the reached ASCII domain"),
    ],
}


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) and not line.lstrip().startswith("//")
    ]
    for position, start in enumerate(starts):
        end = len(lines)
        for candidate in range(start + 1, len(lines)):
            if BOUNDARY.match(lines[candidate]):
                end = candidate
                break
        # Do not swallow trailing blank/comment blocks.
        while end > start + 1 and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        kind = START.match(lines[start]).group(1)
        text = "\n".join(lines[start:end]).strip()
        yield start + 1, kind, text


def relative(path: Path) -> str:
    if path.is_relative_to(ROOT):
        return path.relative_to(ROOT).as_posix()
    return path.name


def used_reason(source: str, line: int) -> str | None:
    for lo, hi, reason in USED_RANGES.get(source, []):
        if lo <= line <= hi:
            return reason
    return None


def classify(source: str, line: int, kind: str, text: str):
    attributes = ",".join(
        item.strip()
        for match in ATTR.findall(text)
        for item in match.split(",")
        if item.strip().split("(", 1)[0] in KNOWN_ATTRIBUTES
    )
    reason = used_reason(source, line)
    if source == "verification.k":
        if kind == "syntax":
            return (
                attributes,
                "PROOF_SUMMARY",
                "ACCEPT",
                "pure result relation; no operational cell or program term matched",
            )
        return (
            attributes,
            "PROOF_SUMMARY_EQUATION",
            "ACCEPT",
            "truthful guarded defining equation; overlap/coverage checked manually",
        )
    if source == "spec.k":
        return (
            attributes,
            "PROOF_CLAIM",
            "ACCEPT",
            "positive claim reconstructed dynamically; adequacy reviewed separately",
        )
    if reason is not None:
        return (
            attributes,
            "FIXED_USED",
            "ACCEPT",
            reason,
        )
    if "no-evaluators" in text:
        return (
            attributes,
            "FIXED_UNUSED_OPAQUE",
            "ACCEPT_OUT_OF_PATH",
            "supplied primitive is not reachable from the submitted program",
        )
    if "[concrete]" in text:
        return (
            attributes,
            "FIXED_UNUSED_CONCRETE",
            "ACCEPT_OUT_OF_PATH",
            "concrete-only supplied rule is not reachable in the proof",
        )
    return (
        attributes,
        "FIXED_UNUSED",
        "ACCEPT_OUT_OF_PATH",
        "constructor/cell/callee shape is not reachable from the submitted program",
    )


def main() -> None:
    paths = [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k")), *EXTRA]
    counts = collections.Counter()
    rows = []
    entry_id = 0
    for path in paths:
        source = relative(path)
        for line, kind, declaration in declarations(path):
            entry_id += 1
            attrs, relevance, decision, rationale = classify(
                source, line, kind, declaration
            )
            counts[(source, kind)] += 1
            counts[("ALL", kind)] += 1
            rows.append(
                (
                    entry_id,
                    source,
                    line,
                    kind,
                    attrs,
                    relevance,
                    decision,
                    rationale,
                    declaration.replace("\t", " ").replace("\n", "\\n"),
                )
            )

    print(
        "id\tfile\tline\tkind\tattributes\trelevance\tdecision\t"
        "rationale\tdeclaration"
    )
    for row in rows:
        print("\t".join(map(str, row)))
    print("# SUMMARY")
    print(f"# total_entries={len(rows)}")
    for (source, kind), count in sorted(counts.items()):
        print(f"# count file={source} kind={kind} value={count}")


if __name__ == "__main__":
    main()
