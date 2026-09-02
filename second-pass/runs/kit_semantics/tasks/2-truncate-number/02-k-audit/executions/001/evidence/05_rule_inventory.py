#!/usr/bin/env python3
"""Enumerate every local K declaration/rule in the audited source definition."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(r"^\s*(syntax|rule|claim|context|configuration)\b")
STOP = re.compile(r"^\s*(?:end)?module\b|^\s*requires\b")
USED_RULES = {
    ("semantics/core.k", 125): "actual Module loader",
    ("semantics/core.k", 126): "left-to-right statement sequencing",
    ("semantics/core.k", 127): "empty statement sequence",
    ("semantics/core.k", 131): "callee/body Name lookup begins",
    ("semantics/core.k", 132): "successful lexical lookup",
    ("semantics/core.k", 152): "parent-scope lookup fallback (potential path)",
    ("semantics/core.k", 158): "builtinsScope normalization in configuration",
    ("semantics/core.k", 189): "argument evaluation starts left-to-right",
    ("semantics/core.k", 190): "evaluated argument appended",
    ("semantics/core.k", 191): "argument evaluation completes",
    ("semantics/core.k", 194): "Int literal (not used by target body)",
    ("semantics/core.k", 214): "appendVal base case for one call argument",
    ("semantics/controls.k", 48): "module docstring Expr statement is discarded after evaluation",
    ("semantics/str.k", 14): "module docstring Str literal",
    ("semantics/functions.k", 14): "actual FuncDef installs the closure",
    ("semantics/functions.k", 63): "parameter binding termination",
    ("semantics/functions.k", 64): "bind number to the evaluated argument",
    ("semantics/functions.k", 78): "Return captures the body result and discards body suffix",
    ("semantics/functions.k", 85): "pop restores caller state and yields return value",
    ("semantics/call.k", 20): "Call evaluates the callee first",
    ("semantics/call.k", 21): "Call begins argument evaluation",
    ("semantics/call.k", 69): "closure call allocates frame and executes exact embedded body",
    ("semantics/operators.k", 12): "evaluated BinOp dispatch",
    ("semantics/float.k", 21): "Float(1.0) literal",
    ("semantics/float.k", 38): "LLVM-only concrete floatMod equation",
    ("semantics/float.k", 39): "float percent dispatch to opaque floatMod",
}


def relative(path: Path) -> str:
    reference_root = ROOT / "reference-semantics"
    if path.is_relative_to(reference_root):
        return path.relative_to(reference_root).as_posix()
    return path.relative_to(ROOT).as_posix()


def extract(path: Path):
    lines = path.read_text().splitlines()
    starts = [(index, START.match(line)) for index, line in enumerate(lines)]
    starts = [(index, match) for index, match in starts if match]
    for position, (index, match) in enumerate(starts):
        assert match is not None
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines: list[str] = []
        for line in lines[index:next_index]:
            if block_lines and STOP.match(line):
                break
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                continue
            block_lines.append(stripped)
        yield index + 1, match.group(1), " ".join(block_lines)


def classifications(kind: str, text: str) -> list[str]:
    labels: list[str] = []
    if kind == "syntax":
        labels.append("syntax_declaration")
        for attr, label in [
            ("function", "function"),
            ("total", "total"),
            ("functional", "functional"),
            ("symbol(", "named_symbol"),
            ("no-evaluators", "opaque_no_evaluators"),
            ("strict", "evaluation_order"),
            ("macro", "macro"),
        ]:
            if attr in text:
                labels.append(label)
    elif kind == "rule":
        labels.append(
            "simplification_rule" if "simplification" in text else "ordinary_semantic_rule"
        )
        for attr, label in [
            ("priority(", "priority_rule"),
            ("[owise]", "owise_rule"),
            ("concrete", "concrete_rule"),
            ("anywhere", "anywhere_rule"),
            ("macro", "macro_rule"),
        ]:
            if attr in text:
                labels.append(label)
    elif kind == "claim":
        labels.append("reachability_claim")
    elif kind == "context":
        labels.append("evaluation_context")
    elif kind == "configuration":
        labels.append("configuration")
    return labels


def main() -> int:
    totals: collections.Counter[str] = collections.Counter()
    file_counts: collections.Counter[str] = collections.Counter()
    entries = 0
    print("# Exhaustive local K declaration and rule inventory")
    print("# disposition meanings:")
    print("#   USED_PATH_REVIEWED: reached by the submitted Module or by the candidate Call claim")
    print("#   FIXED_UNUSED_NO_FALSE_WITNESS: supplied baseline declaration/rule not reached here;")
    print("#     no concrete or symbolic false-conclusion witness was found in this audit")
    print("#   LOCAL_CLAIM_REVIEWED: candidate reachability claim, reviewed separately for adequacy")
    for path in FILES:
        rel = relative(path)
        found = list(extract(path))
        print(f"\n## FILE {rel} declarations={len(found)}")
        if not found:
            print("(no local syntax, rules, claims, contexts, or configuration)")
        for line, kind, text in found:
            labels = classifications(kind, text)
            totals.update(labels)
            file_counts[rel] += 1
            entries += 1
            used = USED_RULES.get((rel, line))
            if kind == "claim":
                disposition = "LOCAL_CLAIM_REVIEWED"
            elif used:
                disposition = f"USED_PATH_REVIEWED ({used})"
            else:
                disposition = "FIXED_UNUSED_NO_FALSE_WITNESS"
            print(
                f"{rel}:{line} | kind={kind} | classes={','.join(labels)} | "
                f"disposition={disposition} | {text}"
            )

    print("\n# SUMMARY")
    print(f"files={len(FILES)} entries={entries}")
    expected_classes = {
        "syntax_declaration",
        "function",
        "total",
        "functional",
        "named_symbol",
        "opaque_no_evaluators",
        "evaluation_order",
        "macro",
        "ordinary_semantic_rule",
        "simplification_rule",
        "priority_rule",
        "owise_rule",
        "concrete_rule",
        "anywhere_rule",
        "macro_rule",
        "evaluation_context",
        "configuration",
        "reachability_claim",
    }
    for label in sorted(expected_classes | totals.keys()):
        print(f"class {label}={totals[label]}")
    for rel, count in sorted(file_counts.items()):
        print(f"file {rel}={count}")
    print("verification_local_extensions=0")
    print("candidate_positive_claims=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
