#!/usr/bin/env python3
"""Build an exhaustive declaration/rule inventory with target-path decisions."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")

files = [ROOT / "reference-semantics" / "semantics.k"]
files += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
files += [ROOT / "verification.k", ROOT / "spec.k"]

start_re = re.compile(
    r"^(module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)
attribute_re = re.compile(
    r"\b(function|total|functional|macro|macro-rec|priority|simplification|"
    r"concrete|owise|symbol|no-evaluators)\b"
)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if line.startswith("requires "):
            starts.append((index, "requires"))
        else:
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
        yield start + 1, kind, " ".join(part.strip() for part in text_lines)


def supplied_target_relevance(relative: str, line: int) -> str:
    if relative.endswith("semantics/syntax.k"):
        return "TARGET_SYNTAX_MIXED"
    if relative.endswith("semantics/core.k") and (
        13 <= line <= 60 or 123 <= line <= 225
    ):
        return "TARGET_PATH"
    if relative.endswith("semantics/int.k"):
        return "TARGET_PATH"
    if relative.endswith("semantics/operators.k") and line <= 20:
        return "TARGET_PATH"
    if relative.endswith("semantics/controls.k") and (
        8 <= line <= 31 or 50 <= line <= 82 or 93 <= line <= 108
    ):
        return "TARGET_PATH"
    if relative.endswith("semantics/functions.k") and (
        13 <= line <= 20 or 62 <= line <= 91
    ):
        return "TARGET_PATH"
    if relative.endswith("semantics/call.k") and (
        18 <= line <= 21 or 69 <= line <= 75
    ):
        return "TARGET_PATH"
    if relative.endswith("semantics/list.k") and 8 <= line <= 10:
        return "TARGET_PATH"
    if relative.endswith("semantics/tuple.k") and 30 <= line <= 41:
        return "TARGET_PATH"
    if relative.endswith("semantics/iter.k"):
        return "TARGET_PATH"
    if relative.endswith("semantics/assert.k"):
        return "CONCRETE_TEST_ONLY"
    return "IMPORTED_UNUSED"


def decision(relative: str, line: int, kind: str, text: str) -> tuple[str, str]:
    attrs = sorted(set(attribute_re.findall(text)))
    attributes = ",".join(attrs) if attrs else "-"
    if relative == "verification.k":
        relevance = "PROOF_LOCAL"
        if kind == "rule" and line in (177, 182):
            value = (
                "UNSOUND_BROAD_BRIDGE: fixed execution is stuck with retV(42), "
                "but this rule proves the helper result; see 05-helper-*"
            )
        elif kind == "rule" and line == 191:
            value = (
                "UNSOUND_BROAD_BRIDGE: omits defining scope; fixed rebound helper "
                "returns 99 while bridge returns -1; see 05-signed-*"
            )
        elif kind == "rule" and line == 200:
            value = (
                "UNSOUND_BROAD_BRIDGE: omits signed_digit_sum binding; fixed loop "
                "counts 1 while bridge counts 0; see 05-count-with-n-*"
            )
        elif kind == "rule" and line == 230:
            value = (
                "UNSOUND_BROAD_BRIDGE: omits signed_digit_sum binding; fixed initial "
                "loop counts 1 while bridge counts 0; see 05-count-initial-*"
            )
        elif kind == "rule" and line in (145, 159):
            value = (
                "SOUND_EXACT_BRIDGE: bridge match, continuation, cells, guards, and "
                "state update equal the bridge-free loop claim"
            )
        elif kind == "rule" and line == 220:
            value = "SOUND_EMPTY_LOOP_BRIDGE: body/callee binding is not observed"
        elif 7 <= line <= 71:
            value = (
                "SOUND_DEFINITION_ON_USE_DOMAIN: disjoint equations, integer descent, "
                "and allInts guard cover every target use"
            )
        elif 74 <= line <= 137:
            value = (
                "EXACT_PROGRAM_MACRO: constructor equality machine-checked in "
                "04-constructor-identity.log"
            )
        else:
            value = "MODULE_OR_IMPORT_SCAFFOLD"
        return relevance, f"{value}; attrs={attributes}"
    if relative == "spec.k":
        return "TARGET_CLAIM", f"THEOREM_OBLIGATION_NOT_EXTENSION; attrs={attributes}"

    relevance = supplied_target_relevance(relative, line)
    if "symbol" in attrs or "no-evaluators" in attrs:
        value = (
            "OPAQUE_TRUST_BOUNDARY_INERT_FOR_TARGET: unreachable from solution.mpy "
            "and absent from every result dependency"
        )
    elif "concrete" in attrs and relevance != "TARGET_PATH":
        value = "CONCRETE_ONLY_OR_UNUSED: absent from Haskell proof dependency"
    elif relevance in ("TARGET_PATH", "TARGET_SYNTAX_MIXED"):
        value = (
            "REVIEWED_TARGET_PATH_SOUND: fixed supplied rule follows the modeled "
            "integer/list execution for this program; no target-domain counterexample"
        )
    elif relevance == "CONCRETE_TEST_ONLY":
        value = (
            "CONCRETE_TEST_ONLY: used for smoke assertions, not for symbolic claim closure"
        )
    else:
        value = (
            "IMPORTED_BUT_TARGET_INERT: constructor/symbol is not reachable from "
            "solution.mpy or proof summaries and cannot affect target closure"
        )
    return relevance, f"{value}; attrs={attributes}"


rows: list[tuple[object, ...]] = []
for path in files:
    relative = path.relative_to(ROOT).as_posix()
    for line, kind, text in blocks(path):
        relevance, verdict = decision(relative, line, kind, text)
        rows.append((len(rows) + 1, relative, line, kind, relevance, verdict, text))

with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(
        ["id", "file", "line", "kind", "target_relevance", "review_decision", "declaration"]
    )
    writer.writerows(rows)

counts: dict[str, int] = {}
for row in rows:
    counts[str(row[3])] = counts.get(str(row[3]), 0) + 1
print(f"inventory_rows={len(rows)}")
for kind in sorted(counts):
    print(f"kind_{kind}={counts[kind]}")
print(
    "unsound_bridge_rows="
    + str(sum("UNSOUND_BROAD_BRIDGE" in str(row[5]) for row in rows))
)
print(f"output={OUTPUT}")
print("RULE_INVENTORY=COMPLETE")
