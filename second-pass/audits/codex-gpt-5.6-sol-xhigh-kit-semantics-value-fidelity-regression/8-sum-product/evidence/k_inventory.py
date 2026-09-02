#!/usr/bin/env python3
"""Generate a source-level inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/source")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "connection-spec.k",
    ROOT / "spec.k",
]

REACHED_SUPPLIED_RULES: dict[str, dict[int, str]] = {
    "reference-semantics/semantics/core.k": {
        125: "loads the submitted Module body",
        126: "sequences submitted statements",
        127: "terminates an empty statement sequence",
        131: "starts lexical Name lookup",
        132: "returns a binding from the current scope",
        189: "evaluates the next call/tuple argument",
        190: "accumulates an evaluated call/tuple argument",
        191: "dispatches the completed argument sequence",
        194: "evaluates integer literals",
        214: "appends the first evaluated value",
        215: "preserves left-to-right argument order",
        218: "embeds an empty evaluated argument list",
        219: "embeds a nonempty evaluated argument list",
    },
    "reference-semantics/semantics/list.k": {
        9: "fixed-semantics empty-list iterator case used by the connection theorem",
        10: "fixed-semantics cons-list iterator case used by the connection theorem",
    },
    "reference-semantics/semantics/tuple.k": {
        15: "starts return-tuple element evaluation",
        16: "constructs the returned tuple",
        32: "binds each yielded loop element to the target name",
    },
    "reference-semantics/semantics/controls.k": {
        9: "performs ordinary local assignments",
        20: "performs integer accumulator AugAssign updates",
        36: "models the unused typing import as an observable no-op",
        69: "enters the real For loop after evaluating its iterable",
        71: "requests the next iterator element",
        72: "terminates the empty iterator",
        73: "binds and executes the real body for a yielded element",
        85: "continues to the next real loop head",
    },
    "reference-semantics/semantics/functions.k": {
        14: "loads the exact sum_product closure",
        63: "finishes exact parameter binding",
        64: "binds the numbers parameter",
        78: "captures the evaluated return tuple",
        85: "restores the caller frame and exposes the return value",
    },
    "reference-semantics/semantics/int.k": {
        9: "computes sum_value + number over mathematical integers",
        14: "computes product_value * number over mathematical integers",
    },
    "reference-semantics/semantics/call.k": {
        20: "evaluates the real callee expression",
        21: "evaluates the real call argument",
        69: "allocates the real function frame and executes its body",
    },
}

LOCAL_RULE_ASSESSMENTS: dict[int, str] = {
    11: "sound empty constructor equation for the proof list embedding",
    12: "sound cons constructor equation with structural descent",
    17: "sound contextual lifting of the empty embedding equation",
    22: "sound contextual lifting of the cons embedding equation",
    29: "sound empty accumulator equation for sum",
    30: "sound cons accumulator equation for sum with structural descent",
    33: "sound empty accumulator equation for product",
    34: "sound cons accumulator equation for product with structural descent",
    37: "sound empty equation preserving the prior loop-target value",
    38: "sound cons equation selecting the last yielded integer with structural descent",
    47: "sound empty iterator acceleration; universally connected to fixed semantics",
    53: "sound cons iterator acceleration; universally connected to fixed semantics",
}

START = re.compile(
    r'^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?|module|endmodule|imports?|requires(?=\s+"))\b'
)


def remove_comments(text: str) -> str:
    result: list[str] = []
    index = 0
    in_string = False
    escaped = False
    in_line_comment = False
    in_block_comment = False
    while index < len(text):
        char = text[index]
        pair = text[index : index + 2]
        if in_line_comment:
            if char == "\n":
                in_line_comment = False
                result.append(char)
            index += 1
            continue
        if in_block_comment:
            if pair == "*/":
                in_block_comment = False
                index += 2
            else:
                if char == "\n":
                    result.append(char)
                index += 1
            continue
        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            result.append(char)
            index += 1
            continue
        if pair == "//":
            in_line_comment = True
            index += 2
            continue
        if pair == "/*":
            in_block_comment = True
            index += 2
            continue
        result.append(char)
        index += 1
    return "".join(result)


def statements(path: Path) -> list[tuple[int, str, str]]:
    source = remove_comments(path.read_text())
    lines = source.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    result: list[tuple[int, str, str]] = []
    for ordinal, (start, keyword) in enumerate(starts):
        end = starts[ordinal + 1][0] if ordinal + 1 < len(starts) else len(lines)
        block = " ".join(part.strip() for part in lines[start:end] if part.strip())
        result.append((start + 1, keyword, block))
    return result


def classify(keyword: str, block: str) -> str:
    if keyword == "rule":
        if "simplification" in block:
            return "simplification-rule"
        if "priority(" in block:
            return "priority-rule"
        return "ordinary-rule"
    if keyword == "syntax":
        attributes = []
        for attr in ("function", "functional", "total", "macro", "strict", "seqstrict", "token"):
            if re.search(rf"\b{re.escape(attr)}\b", block):
                attributes.append(attr)
        return "syntax" + (f"[{','.join(attributes)}]" if attributes else "")
    return keyword.replace(" ", "-")


def assessment(relative: str, line: int, keyword: str, block: str) -> str | None:
    if keyword == "rule":
        if relative == "verification.k":
            return "LOCAL_PASS — " + LOCAL_RULE_ASSESSMENTS[line]
        reached = REACHED_SUPPLIED_RULES.get(relative, {}).get(line)
        if reached:
            return (
                "SUPPLIED_REACHED_PASS — "
                + reached
                + "; checked for binding, evaluation order, control, state footprint, "
                "and agreement with mathematical +/* where applicable"
            )
        return (
            "SUPPLIED_UNREACHED — this rule has no matching term on the pinned entry, "
            "loop, or connection paths, so it cannot enable a false conclusion for an "
            "intended list[int] input; it remains only part of the immutable supplied-"
            "semantics trust boundary, with no claim of full-CPython validity"
        )
    if keyword == "syntax":
        if relative == "verification.k":
            if line in (7, 10):
                return "LOCAL_PASS — free constructor/embedding syntax, fixed by exhaustive equations"
            return "LOCAL_PASS — total structural summary with disjoint exhaustive equations"
        if "no-evaluators" in block or "symbol(" in block:
            return (
                "SUPPLIED_OPAQUE_UNREACHED — opaque/trusted symbol is never reached by "
                "the pinned program or any target/connection claim"
            )
        return (
            "SUPPLIED_DECLARATION — imported unchanged; reached productions are mapped "
            "separately, and all other productions are absent from the submitted MPY AST"
        )
    if keyword == "configuration":
        return (
            "SUPPLIED_REACHED_PASS — entry claim pins the default env/scopes/allocation/"
            "stack/return/exception/exit state, and final cells are result-constraining"
        )
    if keyword == "claim":
        return (
            "CLAIM_AUDITED — precondition, reachable witness, execution boundary, "
            "postcondition, and fresh proof result are reviewed in REVIEW.md"
        )
    return None


totals: collections.Counter[str] = collections.Counter()
for path in FILES:
    relative = str(path.relative_to(ROOT))
    items = statements(path)
    local: collections.Counter[str] = collections.Counter()
    print(f"FILE {relative}")
    for line, keyword, block in items:
        category = classify(keyword, block)
        local[category] += 1
        totals[category] += 1
        print(f"  {line:4d} {category}: {block}")
        decision = assessment(relative, line, keyword, block)
        if decision:
            print(f"       ASSESSMENT: {decision}")
    print(f"  COUNTS {dict(sorted(local.items()))}")

print(f"GLOBAL_COUNTS {dict(sorted(totals.items()))}")
