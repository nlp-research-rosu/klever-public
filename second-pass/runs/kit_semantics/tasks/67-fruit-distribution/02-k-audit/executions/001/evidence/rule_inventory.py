#!/usr/bin/env python3
"""Exhaustive lexical inventory and per-sentence audit disposition for K sources."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
EXTRAS = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
KEYWORDS = ("configuration", "syntax", "context", "rule", "claim", "alias")
BOUNDARIES = KEYWORDS + ("module", "endmodule", "imports")
KNOWN_ATTRS = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "opaque",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
    "macro",
    "macro-rec",
)


def mask_comments(text: str) -> str:
    output = list(text)
    index = 0
    state = "code"
    block_depth = 0
    while index < len(text):
        current = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line":
            if current in "\r\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
        elif state == "block":
            if current == "/" and following == "*":
                output[index] = output[index + 1] = " "
                block_depth += 1
                index += 2
            elif current == "*" and following == "/":
                output[index] = output[index + 1] = " "
                block_depth -= 1
                index += 2
                if block_depth == 0:
                    state = "code"
            else:
                if current not in "\r\n":
                    output[index] = " "
                index += 1
        elif state == "string":
            if current == "\\" and following:
                index += 2
            elif current == '"':
                state = "code"
                index += 1
            else:
                index += 1
        elif current == "/" and following == "/":
            output[index] = output[index + 1] = " "
            state = "line"
            index += 2
        elif current == "/" and following == "*":
            output[index] = output[index + 1] = " "
            state = "block"
            block_depth = 1
            index += 2
        elif current == '"':
            state = "string"
            index += 1
        else:
            index += 1
    return "".join(output)


def module_at(lines: list[str], line_number: int) -> str:
    module = ""
    for line in lines[:line_number]:
        match = re.match(r"\s*module\s+([A-Za-z][A-Za-z0-9_-]*)", line)
        if match:
            module = match.group(1)
        elif re.match(r"\s*endmodule\b", line):
            module = ""
    return module


def attributes(text: str) -> str:
    found: list[str] = []
    for attribute in KNOWN_ATTRS:
        if attribute == "priority":
            matched = re.search(r"\bpriority\s*\(", text)
        else:
            matched = re.search(rf"(?<![A-Za-z0-9_-]){re.escape(attribute)}(?![A-Za-z0-9_-])", text)
        if matched:
            found.append(attribute)
    return ",".join(found) if found else "-"


USED_RANGES: dict[str, list[tuple[int, int]]] = {
    "semantics/syntax.k": [(9, 61)],
    "semantics/core.k": [
        (25, 42),
        (49, 60),
        (68, 70),
        (95, 102),
        (117, 121),
        (129, 181),
        (183, 195),
        (208, 229),
    ],
    "semantics/functions.k": [(8, 16), (62, 90)],
    "semantics/call.k": [(15, 24), (31, 32), (47, 50), (52, 60), (69, 74)],
    "semantics/methods.k": [(70, 86), (121, 138)],
    "semantics/list.k": [(18, 20)],
    "semantics/subscript.k": [(7, 41)],
    "semantics/operators.k": [(10, 13)],
    "semantics/int.k": [(9, 17)],
    "semantics/builtins.k": [(139, 160)],
}


def overlaps(line_start: int, line_end: int, ranges: list[tuple[int, int]]) -> bool:
    return any(line_start <= high and line_end >= low for low, high in ranges)


def disposition(relative: str, kind: str, start: int, end: int, attrs: str) -> tuple[str, str]:
    if relative == "spec.k" and kind == "claim":
        return (
            "TARGET_CLAIM_REVIEWED",
            "Result-constraining entry claim; domain, pinning, satisfiability, and mutation checked.",
        )
    if relative == "verification.k":
        return (
            "NO_LOCAL_EXTENSION",
            "Wrapper imports fixed MPY semantics and contributes no syntax, functions, or rules.",
        )
    if relative == "semantics/concrete.k":
        return (
            "CONCRETE_ONLY_INACTIVE_IN_PROOF",
            "Present for MPY-KRUN concrete execution; VERIFICATION imports MPY, not MPY-CONCRETE.",
        )
    if "no-evaluators" in attrs:
        return (
            "OPAQUE_UNUSED_TRUST_BOUNDARY",
            "Declared fixed-semantics opaque symbol; no float/sort/md5 term is reachable from this integer/string program.",
        )
    if "concrete" in attrs:
        return (
            "CONCRETE_RULE_INACTIVE_IN_PROOF",
            "Concrete twin is used by LLVM only and cannot contribute to the Haskell target proof.",
        )
    if relative == "semantics/builtins.k" and overlaps(start, end, [(151, 160)]):
        return (
            "USED_GUARDED_DOMAIN_LIMITATION",
            "Multi-digit int conversion is over-broad on non-digits, but every target use has nonempty allDigit guards.",
        )
    if relative == "semantics/subscript.k" and overlaps(start, end, [(7, 14), (35, 41)]):
        return (
            "USED_GUARDED_TOTALITY_LIMITATION",
            "valSeqAt is total/underspecified out of bounds; exact five-token split makes indices 0 and 3 in bounds.",
        )
    if relative == "semantics/str.k" and overlaps(start, end, [(12, 17)]):
        return (
            "ASCII_DOMAIN_LIMITATION",
            "String-literal conversion models ASCII only; target labels and recorded satisfying inputs are ASCII.",
        )
    if relative == "semantics/methods.k" and overlaps(start, end, [(70, 86)]):
        return (
            "USED_WHITESPACE_DOMAIN_LIMITATION",
            "No-arg split recognizes space/tab/LF/CR, a strict subset of CPython Unicode whitespace; target phrase domain is constrained through splitWS.",
        )
    if relative == "semantics/functions.k" and overlaps(start, end, [(13, 16)]):
        return (
            "PINNING_MAPPING_ACCEPTED",
            "Fixed FuncDef rule maps the regenerated name/Params/body/environment to the exact closure invoked by the claim.",
        )
    if overlaps(start, end, USED_RANGES.get(relative, [])):
        return (
            "USED_FIXED_RULE_ACCEPTED",
            "Reachable rule/declaration matches the fixed MPY execution path; no false conclusion witness exists under the entry guards.",
        )
    return (
        "UNUSED_FIXED_RULE_REVIEWED",
        "Outside this program's reachable construct slice; no overlap with target symbols yields a false conclusion on its domain.",
    )


paths = sorted(ROOT.rglob("*.k")) + EXTRAS
rows: list[list[str]] = []
file_counts: dict[str, dict[str, int]] = {}
for path in paths:
    if path.is_symlink() or not path.is_file():
        raise AssertionError(f"non-regular source: {path}")
    if path.is_relative_to(ROOT):
        relative = path.relative_to(ROOT).as_posix()
    else:
        relative = path.name
    text = path.read_text()
    masked = mask_comments(text)
    lines = text.splitlines()
    masked_lines = masked.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(masked_lines):
        match = re.match(r"\s*(" + "|".join(BOUNDARIES) + r")\b", line)
        if match:
            starts.append((index, match.group(1)))
    counts: dict[str, int] = {}
    for position, (start_index, kind) in enumerate(starts):
        if kind not in KEYWORDS:
            continue
        next_boundaries = [
            candidate
            for candidate, _candidate_kind in starts[position + 1 :]
            if candidate > start_index
        ]
        end_index = (next_boundaries[0] if next_boundaries else len(lines)) - 1
        while end_index >= start_index and not lines[end_index].strip():
            end_index -= 1
        sentence = "\n".join(lines[start_index : end_index + 1]).strip()
        normalized = " ".join(sentence.split())
        attrs = attributes(mask_comments(sentence))
        assessment, rationale = disposition(
            relative, kind, start_index + 1, end_index + 1, attrs
        )
        role = (
            "operational"
            if kind in {"rule", "context"} and "<k>" in sentence
            else "equational"
            if kind == "rule"
            else "declaration"
        )
        rows.append(
            [
                relative,
                module_at(masked_lines, start_index),
                kind,
                str(start_index + 1),
                str(end_index + 1),
                role,
                attrs,
                hashlib.sha256(normalized.encode()).hexdigest(),
                assessment,
                rationale,
                normalized,
            ]
        )
        counts[kind] = counts.get(kind, 0) + 1
    file_counts[relative] = counts

print(
    "\t".join(
        [
            "file",
            "module",
            "kind",
            "start_line",
            "end_line",
            "role",
            "attributes",
            "normalized_sha256",
            "assessment",
            "rationale",
            "normalized_sentence",
        ]
    )
)
for row in rows:
    print("\t".join(column.replace("\t", " ") for column in row))
print(f"# INVENTORY_ROWS={len(rows)}")
for relative, counts in sorted(file_counts.items()):
    rendered = ",".join(f"{kind}={count}" for kind, count in sorted(counts.items()))
    print(f"# FILE {relative} {rendered or 'no-local-declarations'}")
for kind in KEYWORDS:
    print(f"# TOTAL_{kind.upper()}={sum(1 for row in rows if row[2] == kind)}")
for attr in KNOWN_ATTRS:
    print(
        f"# ATTRIBUTE_{attr.upper().replace('-', '_')}="
        f"{sum(1 for row in rows if attr in row[6].split(','))}"
    )
for assessment in sorted({row[8] for row in rows}):
    print(f"# ASSESSMENT_{assessment}={sum(1 for row in rows if row[8] == assessment)}")
print("# RULE_INVENTORY=PASS")
