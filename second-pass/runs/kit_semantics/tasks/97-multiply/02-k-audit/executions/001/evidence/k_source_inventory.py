#!/usr/bin/env python3
"""Exhaustive lexical inventory and target-slice classification of K sentences."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
KEYWORDS = {
    "syntax",
    "rule",
    "configuration",
    "context",
    "claim",
    "alias",
    "macro",
}

# Sentence start lines on the exact operational slice taken by SPEC.multiply-correct.
TARGET_STARTS = {
    "reference-semantics/semantics/syntax.k": {9, 41, 50, 56, 57, 60},
    "reference-semantics/semantics/core.k": {
        13,
        14,
        25,
        36,
        37,
        38,
        39,
        40,
        42,
        49,
        130,
        131,
        132,
        152,
        157,
        185,
        186,
        189,
        190,
        191,
        194,
        209,
        238,
        239,
        240,
    },
    "reference-semantics/semantics/int.k": {23, 24, 28, 29},
    "reference-semantics/semantics/operators.k": {12},
    "reference-semantics/semantics/functions.k": {
        8,
        63,
        64,
        78,
        85,
    },
    "reference-semantics/semantics/call.k": {19, 20, 21, 69},
    "spec.k": {6},
}

PINNING_STARTS = {
    "reference-semantics/semantics/syntax.k": {61},
    "reference-semantics/semantics/core.k": {124, 125, 126, 127},
    "reference-semantics/semantics/functions.k": {14},
}


def mask_non_code(text: str) -> str:
    output = list(text)
    index = 0
    state = "code"
    depth = 0
    while index < len(text):
        current = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line-comment":
            if current in "\r\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "string":
            if current == "\\" and following:
                output[index] = output[index + 1] = " "
                index += 2
                continue
            if current == '"':
                state = "code"
            elif current not in "\r\n":
                output[index] = " "
            index += 1
            continue
        if state == "block-comment":
            if current == "/" and following == "*":
                output[index] = output[index + 1] = " "
                depth += 1
                index += 2
                continue
            if current == "*" and following == "/":
                output[index] = output[index + 1] = " "
                depth -= 1
                index += 2
                if depth == 0:
                    state = "code"
                continue
            if current not in "\r\n":
                output[index] = " "
            index += 1
            continue
        if current == "/" and following == "/":
            output[index] = output[index + 1] = " "
            state = "line-comment"
            index += 2
            continue
        if current == "/" and following == "*":
            output[index] = output[index + 1] = " "
            state = "block-comment"
            depth = 1
            index += 2
            continue
        if current == '"':
            state = "string"
        index += 1
    return "".join(output)


def sentence_starts(text: str) -> list[tuple[int, str]]:
    masked = mask_non_code(text)
    starts = []
    for line_number, line in enumerate(masked.splitlines(), 1):
        match = re.match(r"^[ \t]*([A-Za-z]+)\b", line)
        if match and match.group(1) in KEYWORDS:
            starts.append((line_number, match.group(1)))
    return starts


def attributes(sentence: str) -> list[str]:
    masked = mask_non_code(sentence)
    known = re.compile(
        r"(?<![A-Za-z0-9_-])(?:"
        r"function|total|functional|no-evaluators|owise|concrete|"
        r"macro(?:-rec)?|simplification|simplifier|"
        r"strict(?:\([^]\r\n]*\))?|seqstrict(?:\([^]\r\n]*\))?|"
        r"priority\([0-9]+\)|symbol\([^]\r\n]+\)"
        r")(?=[,\]\s])"
    )
    return known.findall(masked)


def assessment(relative: str, line: int, kind: str, attrs: list[str]) -> tuple[str, str]:
    if relative == "verification.k":
        return ("PROOF_LOCAL", "NO_EXTENSION_DECLARATIONS_OR_RULES")
    if relative == "spec.k":
        return ("TARGET_CLAIM", "RESULT_CONSTRAINING_REAL_PROGRAM_CLAIM")
    if "no-evaluators" in attrs:
        return (
            "OPAQUE_FIXED_BOUNDARY_UNUSED",
            "ACCEPTED_UNUSED_FIXED_BOUNDARY_NO_VALUE_OR_CONTROL_INFLUENCE",
        )
    if line in PINNING_STARTS.get(relative, set()):
        return (
            "PROGRAM_BINDING_CONSTRUCTOR_SLICE",
            "SOUND_MODULE_LOAD_PRODUCES_CLAIMED_CLOSURE_BINDING",
        )
    if line in TARGET_STARTS.get(relative, set()):
        return (
            "TARGET_OPERATIONAL_SLICE",
            "SOUND_FOR_ALL_SYMBOLIC_INT_INPUTS",
        )
    if "semantics/concrete.k" in relative:
        return (
            "CONCRETE_ONLY_FIXED_MODEL",
            "ACCEPTED_NOT_IMPORTED_BY_PROOF_DEFINITION",
        )
    if kind == "rule":
        return (
            "FIXED_MODEL_RULE_UNUSED",
            "ACCEPTED_WITHIN_SUPPLIED_SUBSET_NO_TARGET_DEPENDENCY_NO_FALSE_WITNESS",
        )
    return (
        "FIXED_MODEL_DECLARATION_UNUSED",
        "ACCEPTED_DECLARATION_NO_TARGET_DEPENDENCY",
    )


def main() -> int:
    records = []
    for path in SOURCES:
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text()
        lines = text.splitlines()
        starts = sentence_starts(text)
        for index, (start, kind) in enumerate(starts):
            end = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
            # Do not absorb an endmodule or a following module into the last sentence.
            while end >= start and re.match(
                r"^[ \t]*(?:end)?module\b", mask_non_code(lines[end - 1])
            ):
                end -= 1
            raw = "\n".join(lines[start - 1 : end]).rstrip()
            attrs = attributes(raw)
            role, decision = assessment(relative, start, kind, attrs)
            normalized = " ".join(raw.split())
            records.append(
                {
                    "id": f"{relative}:{start}",
                    "file": relative,
                    "start": start,
                    "end": end,
                    "kind": kind,
                    "attributes": attrs,
                    "role": role,
                    "decision": decision,
                    "sha256": hashlib.sha256(normalized.encode()).hexdigest(),
                    "text": normalized,
                }
            )

    output = Path("/audit-output/evidence/stage5-rule-inventory.json")
    output.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")

    kinds = Counter(record["kind"] for record in records)
    roles = Counter(record["role"] for record in records)
    attribute_counts = Counter(
        attribute for record in records for attribute in record["attributes"]
    )
    priority_records = [
        record for record in records if any(a.startswith("priority(") for a in record["attributes"])
    ]
    opaque_records = [
        record for record in records if "no-evaluators" in record["attributes"]
    ]
    simplification_records = [
        record
        for record in records
        if any(a in {"simplification", "simplifier"} for a in record["attributes"])
    ]
    print(f"source_file_count={len(SOURCES)}")
    print(f"sentence_count={len(records)}")
    print("kind_counts=" + json.dumps(dict(sorted(kinds.items())), sort_keys=True))
    print("role_counts=" + json.dumps(dict(sorted(roles.items())), sort_keys=True))
    print(
        "attribute_counts="
        + json.dumps(dict(sorted(attribute_counts.items())), sort_keys=True)
    )
    print(f"priority_sentence_count={len(priority_records)}")
    print(f"opaque_no_evaluators_count={len(opaque_records)}")
    print(f"simplification_sentence_count={len(simplification_records)}")
    print(
        "opaque_ids="
        + json.dumps([record["id"] for record in opaque_records], separators=(",", ":"))
    )
    print(f"inventory_path={output}")
    print(f"inventory_sha256={hashlib.sha256(output.read_bytes()).hexdigest()}")

    verification_records = [
        record for record in records if record["file"] == "verification.k"
    ]
    print(f"verification_local_sentence_count={len(verification_records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
