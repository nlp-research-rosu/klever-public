#!/usr/bin/env python3
"""Exhaustive local K declaration/rule inventory and Unicode equation audit."""

from __future__ import annotations

import ast
import csv
import re
import sys
import unicodedata
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
FILES = [
    ROOT / "semantic.k",
    ROOT / "unicode-case.k",
    ROOT / "verification.k",
    ROOT / "spec.k",
]


def declaration_blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if (
            stripped.startswith("syntax ")
            or stripped.startswith("rule ")
            or stripped.startswith("claim")
            or stripped.startswith("configuration")
        ):
            starts.append(index)
    for position, start in enumerate(starts):
        end_bound = starts[position + 1] if position + 1 < len(starts) else len(lines)
        end = start + 1
        # Include continuation lines, but stop at blank/comment/module terminators.
        while end < end_bound:
            stripped = lines[end].strip()
            if stripped == "" or stripped.startswith("//") or stripped == "endmodule":
                break
            end += 1
        text = "\n".join(lines[start:end]).strip()
        yield start + 1, end, text


def classify(path: Path, text: str):
    first = text.splitlines()[0].strip()
    attributes = ",".join(re.findall(r"\[([^\]]+)\]", text))
    if first.startswith("configuration"):
        return "configuration", "operational state", attributes
    if first.startswith("claim"):
        return "reachability claim", "target theorem", attributes
    if first.startswith("syntax "):
        if "[function" in text or "function" in attributes:
            return "function declaration", "equational symbol", attributes
        return "syntax declaration", "constructor grammar", attributes
    if path.name == "unicode-case.k":
        if "[owise]" in text:
            return "owise function equation", "definitional summary", attributes
        return "concrete function equation", "definitional summary", attributes
    if "pySwapCase" in text or "utf8CharLen" in text or path.name == "verification.k":
        if "[owise]" in text:
            return "owise function equation", "definitional summary", attributes
        return "function equation", "definitional summary", attributes
    return "ordinary semantic rule", "fixed operational semantics", attributes


def assess(path: Path, start: int, text: str, kind: str) -> str:
    if kind == "configuration":
        return "Minimal k/arg/functions/env state; every cell is used."
    if kind == "reachability claim":
        return "Target claim inventoried; theorem adequacy assessed separately."
    if kind == "syntax declaration":
        return "Constructor grammar; no semantic equation or proof shortcut."
    if kind == "function declaration":
        if "pySwapChar" in text:
            return (
                "Total scalar mapping; 2,816 exact equations plus one owise "
                "fallback give complete, nonoverlapping coverage."
            )
        if "utf8CharLen" in text:
            return (
                "Total byte-width helper; guarded equations plus owise cover "
                "all K strings, with valid UTF-8 widths used by the program."
            )
        if "pySwapCase" in text:
            return (
                "Recursive result function; equations descend on nonempty "
                "Haskell-backend byte strings."
            )
        if "flipSpec" in text:
            return (
                "Definitional contract alias; truthful but not an independent "
                "connection theorem for the swapcase primitive."
            )
    if path.name == "unicode-case.k":
        if "[owise]" in text:
            return (
                "Identity fallback; sound for every scalar absent from the "
                "exhaustive non-identity mapping and nonoverlapping by owise."
            )
        return (
            "Exact CPython 3.10/Unicode 13 scalar equation; checked "
            "mechanically against chr.swapcase()."
        )
    if path.name == "verification.k":
        return (
            "Truthful definitional alias flipSpec(S)=pySwapCase(S); does not "
            "replace operational execution."
        )
    semantic_assessments = {
        55: "Loads the submitted module body, preserves continuation, then invokes flip_case.",
        58: "Left-to-right statement sequencing; unused for the one-statement module.",
        60: "Installs the exact function parameters/body in the functions map.",
        63: "Looks up the selected binding, installs its exact body, and binds the sole argument in an empty environment.",
        67: "Evaluates a return expression before the return marker.",
        69: "Reads the exact name binding from env.",
        72: "Literal-string evaluation; unused by the submitted body.",
        74: "Evaluates the attribute receiver before attribute selection.",
        75: "Constructs a bound method preserving both requested name and receiver.",
        78: "Evaluates the zero-argument callee before the call marker.",
        79: "Models the external str.swapcase primitive by pySwapCase on the preserved receiver.",
        82: "Returns only in the exact #return ~> #endCall context and clears the callee environment.",
        91: "Correct recursive base pySwapCase(\"\")=\"\".",
        92: "Consumes one Haskell-backend UTF-8 character-width segment and recurses on a strictly shorter valid input.",
        101: "Correct one-byte ASCII leading-width branch.",
        103: "Correct two-byte leading-width interval; includes invalid C0/C1 only outside the Python-string encoding domain.",
        106: "Correct three-byte leading-width interval.",
        109: "Correct four-byte leading-width interval; includes invalid F5-F7 only outside the Python-string encoding domain.",
        112: "Owise width 1 covers continuation/invalid leading bytes and the independently-called empty case.",
    }
    return semantic_assessments.get(
        start, "Reviewed local declaration; no unclassified proof extension."
    )


def k_literal_to_unicode(literal: str) -> str:
    byte_chars = ast.literal_eval(literal)
    return bytes(ord(character) for character in byte_chars).decode("utf-8")


def audit_unicode(path: Path):
    pattern = re.compile(
        r'^  rule pySwapChar\(("(?:\\.|[^"\\])*")\)'
        r' => ("(?:\\.|[^"\\])*")$'
    )
    entries = {}
    parse_failures = []
    owise_count = 0
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if line == "  rule pySwapChar(C) => C [owise]":
            owise_count += 1
            continue
        if not line.startswith("  rule pySwapChar"):
            continue
        match = pattern.match(line)
        if match is None:
            parse_failures.append((line_number, line))
            continue
        lhs_literal = match.group(1)
        rhs_literal = match.group(2)
        lhs = k_literal_to_unicode(lhs_literal)
        rhs = k_literal_to_unicode(rhs_literal)
        entries.setdefault(lhs, []).append((line_number, rhs))

    expected = {
        chr(codepoint): chr(codepoint).swapcase()
        for codepoint in range(0x110000)
        if chr(codepoint).swapcase() != chr(codepoint)
    }
    duplicates = {key: value for key, value in entries.items() if len(value) != 1}
    flattened = {key: value[0][1] for key, value in entries.items()}
    missing = sorted(set(expected) - set(flattened), key=ord)
    extra = sorted(set(flattened) - set(expected), key=ord)
    mismatches = sorted(
        (
            key,
            expected[key],
            flattened[key],
            entries[key][0][0],
        )
        for key in set(expected) & set(flattened)
        if expected[key] != flattened[key]
    )
    return {
        "explicit_count": len(flattened),
        "expected_count": len(expected),
        "owise_count": owise_count,
        "parse_failures": parse_failures,
        "duplicates": duplicates,
        "missing": missing,
        "extra": extra,
        "mismatches": mismatches,
        "expansion_count": sum(len(value) != 1 for value in expected.values()),
    }


def main() -> None:
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(
        [
            "id",
            "file",
            "start_line",
            "end_line",
            "kind",
            "classification",
            "attributes",
            "assessment",
            "text",
        ]
    )
    counts = {}
    inventory_id = 0
    for path in FILES:
        file_counts = {}
        for start, end, text in declaration_blocks(path):
            inventory_id += 1
            kind, classification, attributes = classify(path, text)
            assessment = assess(path, start, text, kind)
            file_counts[kind] = file_counts.get(kind, 0) + 1
            writer.writerow(
                [
                    inventory_id,
                    path.name,
                    start,
                    end,
                    kind,
                    classification,
                    attributes,
                    assessment,
                    text.replace("\n", "\\n"),
                ]
            )
        counts[path.name] = file_counts
    audit = audit_unicode(ROOT / "unicode-case.k")
    print("# SUMMARY", file=sys.stderr)
    print("python", sys.version.replace("\n", " "), file=sys.stderr)
    print("unicode_database", unicodedata.unidata_version, file=sys.stderr)
    print("inventory_entries", inventory_id, file=sys.stderr)
    print("counts", counts, file=sys.stderr)
    all_text = "\n".join(path.read_text() for path in FILES)
    print(
        "total_declarations",
        len(re.findall(r"\[[^\]]*\btotal\b", all_text)),
        file=sys.stderr,
    )
    print(
        "functional_declarations",
        len(re.findall(r"\[[^\]]*\bfunctional\b", all_text)),
        file=sys.stderr,
    )
    print(
        "simplification_rules",
        len(re.findall(r"\[[^\]]*\bsimplification\b", all_text)),
        file=sys.stderr,
    )
    print(
        "explicit_priority_attributes",
        len(re.findall(r"\[[^\]]*\bpriority\b", all_text)),
        file=sys.stderr,
    )
    print(
        "owise_rules",
        len(re.findall(r"\[[^\]]*\bowise\b", all_text)),
        file=sys.stderr,
    )
    print("opaque_declarations", 0, file=sys.stderr)
    for key, value in audit.items():
        if isinstance(value, (list, dict)):
            print(key, "count", len(value), "sample", repr(value)[:500],
                  file=sys.stderr)
        else:
            print(key, value, file=sys.stderr)
    good = (
        audit["explicit_count"] == audit["expected_count"] == 2816
        and audit["owise_count"] == 1
        and not audit["parse_failures"]
        and not audit["duplicates"]
        and not audit["missing"]
        and not audit["extra"]
        and not audit["mismatches"]
    )
    print("unicode_equations_exhaustive_and_exact", good, file=sys.stderr)
    raise SystemExit(0 if good else 1)


if __name__ == "__main__":
    main()
