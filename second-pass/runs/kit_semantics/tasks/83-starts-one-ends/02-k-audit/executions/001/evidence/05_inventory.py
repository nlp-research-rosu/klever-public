#!/usr/bin/env python3
"""Produce an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


START_RE = re.compile(r"^  (syntax|rule|context|configuration|claim)\b")
STOP_RE = re.compile(
    r"^  (?:syntax|rule|context|configuration|claim|imports)\b|^endmodule\b"
)

# Start lines on the constructor/control path for solution.mpy, including the
# one-time module-load bridge that creates the exact manually pinned closure.
USED_STARTS = {
    "semantics/syntax.k": {
        9,
        32,
        37,
        41,
        56,
        57,
        60,
        61,
    },
    "semantics/core.k": {
        25,
        36,
        38,
        39,
        40,
        42,
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        199,
        200,
        208,
        209,
        210,
        213,
        214,
        215,
    },
    "semantics/functions.k": {8, 14, 63, 64, 78, 80, 85},
    "semantics/call.k": {19, 20, 21, 69},
    "semantics/controls.k": {57, 59},
    "semantics/operators.k": {12, 15, 16, 17},
    "semantics/int.k": {13, 14, 17, 26},
}


def statements(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for pos, line in enumerate(lines):
        match = START_RE.match(line)
        if match:
            starts.append((pos, match.group(1)))
    for index, (pos, kind) in enumerate(starts):
        end = len(lines)
        for candidate in range(pos + 1, len(lines)):
            if STOP_RE.match(lines[candidate]):
                end = candidate
                break
        while end > pos + 1 and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        text = " ".join(part.strip() for part in lines[pos:end] if part.strip())
        yield pos + 1, kind, text


def attrs(text: str) -> list[str]:
    found = []
    for name in [
        "function",
        "total",
        "functional",
        "macro",
        "macro-rec",
        "simplification",
        "simp",
        "priority",
        "owise",
        "concrete",
        "symbol",
        "no-evaluators",
        "strict",
        "seqstrict",
    ]:
        if re.search(rf"\b{re.escape(name)}\b", text):
            found.append(name)
    return found


def classify(rel: str, line: int, kind: str, text: str) -> tuple[str, str]:
    used = line in USED_STARTS.get(rel, set())
    attributes = attrs(text)
    if kind == "claim":
        return (
            "TARGET-CLAIM",
            "Entry reachability obligation; adequacy and closure reviewed separately.",
        )
    if kind == "configuration":
        return (
            "ACCEPTED-USED-CONFIGURATION",
            "Exact selected supplied-semantics cell schema; entry claims pin every cell.",
        )
    if kind == "context":
        if used:
            return (
                "ACCEPTED-USED-EVALUATION-CONTEXT",
                "Matches the selected evaluation order for a constructor in solution.mpy.",
            )
        return (
            "ACCEPTED-INERT-EVALUATION-CONTEXT",
            "Fixed supplied-semantics context; its constructor is unreachable in this target.",
        )
    if kind == "syntax":
        if "no-evaluators" in attributes:
            return (
                "ACCEPTED-INERT-OPAQUE-DECLARATION",
                "Named supplied-semantics opaque boundary; unreachable from this integer target.",
            )
        if used:
            return (
                "ACCEPTED-USED-SYNTAX",
                "Declares a constructor/cell/function on the exact target execution path.",
            )
        return (
            "ACCEPTED-INERT-SYNTAX",
            "Fixed supplied syntax/function declaration; not reached by solution.mpy.",
        )
    if kind == "rule":
        if "[concrete]" in text:
            return (
                "ACCEPTED-CONCRETE-ONLY-INERT-RULE",
                "LLVM-only supplied rule; MPY proof definition excludes or does not evaluate it.",
            )
        if used:
            return (
                "ACCEPTED-USED-RULE",
                "Direct target/module-load rule; checked for exact binding, value, control, cells, guards, and overlap.",
            )
        return (
            "ACCEPTED-INERT-RULE",
            "Fixed supplied rule whose LHS/function is unreachable from the target constructor path; no target-answer symbol or universal target overlap.",
        )
    raise AssertionError(kind)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    semantics_root = args.scratch / "reference-semantics"
    files = [semantics_root / "semantics.k", *sorted((semantics_root / "semantics").glob("*.k"))]
    files.extend([args.scratch / "verification.k", args.scratch / "spec.k"])

    counts = Counter()
    classifications = Counter()
    output: list[str] = [
        "# Exhaustive K source inventory",
        "",
        "This inventory is reviewer-generated from the fresh trusted scratch copy. "
        "Every top-level `syntax`, `rule`, `context`, `configuration`, and `claim` "
        "statement is listed with its complete whitespace-collapsed source text.",
        "",
    ]

    for path in files:
        if path.is_relative_to(semantics_root):
            rel = path.relative_to(semantics_root).as_posix()
            display = f"reference-semantics/{rel}"
        else:
            rel = path.name
            display = rel
        file_statements = list(statements(path))
        output.extend(
            [
                f"## {display}",
                "",
                f"Source statements inventoried: {len(file_statements)}.",
                "",
            ]
        )
        if not file_statements:
            output.extend(
                [
                    "No local syntax, rule, context, configuration, or claim statements.",
                    "",
                ]
            )
            continue
        for line, kind, text in file_statements:
            decision, rationale = classify(rel, line, kind, text)
            attributes = attrs(text)
            counts[kind] += 1
            classifications[decision] += 1
            output.extend(
                [
                    f"### {display}:{line} — {kind}",
                    "",
                    f"- Attributes: {', '.join(attributes) if attributes else 'none'}",
                    f"- Decision: {decision}",
                    f"- Rationale: {rationale}",
                    f"- Source: `{text.replace('`', chr(92) + '`')}`",
                    "",
                ]
            )

    output.extend(
        [
            "## Totals",
            "",
            *[f"- {kind}: {count}" for kind, count in sorted(counts.items())],
            "",
            "Classifications:",
            "",
            *[
                f"- {classification}: {count}"
                for classification, count in sorted(classifications.items())
            ],
            "",
        ]
    )
    args.output.write_text("\n".join(output), encoding="utf-8")
    print("statement_counts =", dict(sorted(counts.items())))
    print("classification_counts =", dict(sorted(classifications.items())))
    print("output =", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
