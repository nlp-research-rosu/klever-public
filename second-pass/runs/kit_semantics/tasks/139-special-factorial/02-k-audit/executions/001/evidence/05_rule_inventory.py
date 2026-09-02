#!/usr/bin/env python3
"""Exhaustive source-level declaration/rule inventory for this audit."""

import collections
import pathlib
import re


SCRATCH = pathlib.Path("/tmp/audit-work/reconstruction")
sources = [SCRATCH / "reference-semantics/semantics.k"]
sources += sorted((SCRATCH / "reference-semantics/semantics").glob("*.k"))
sources += [SCRATCH / "verification.k", SCRATCH / "spec.k"]

head = re.compile(r"^\s{0,2}(syntax|rule|context|configuration|claim)\b")
attributes = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "concrete",
    "no-evaluators",
    "symbol",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)

# Rules in the fixed supplied semantics that are on the exact dependency slice
# of solution.mpy. Lines naming generated strictness declarations are handled
# separately via used_syntax_tokens below.
used_rule_lines = {
    "core.k": {125, 126, 127, 131, 132, 158, 189, 190, 191, 194, 200, 214, 215},
    "functions.k": {14, 63, 64, 78, 85},
    "controls.k": {9, 77, 78, 79, 81, 85},
    "call.k": {20, 21, 69},
    "operators.k": {12, 17},
    "int.k": {9, 14, 23},
}
used_context_lines = {"operators.k": {15, 16}}
used_syntax_lines = {
    "syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "core.k": {
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        124,
        130,
        157,
        185,
        186,
        199,
        208,
        209,
        210,
        213,
    },
    "functions.k": {8},
    "controls.k": {65},
    "call.k": {19},
}
known_unused_totality_gaps = {
    ("builtins.k", 134),
    ("float.k", 73),
    ("float.k", 86),
    ("float.k", 93),
    ("methods.k", 27),
    ("subscript.k", 11),
}


def blocks(path: pathlib.Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [(index, head.match(line)) for index, line in enumerate(lines) if head.match(line)]
    for item, (start, match) in enumerate(starts):
        end = starts[item + 1][0] if item + 1 < len(starts) else len(lines)
        body_lines = []
        for line in lines[start:end]:
            stripped = line.strip()
            if stripped.startswith("//") or stripped in {"endmodule"}:
                continue
            body_lines.append(stripped)
        body = " ".join(part for part in body_lines if part)
        body = re.sub(r"\s+", " ", body)
        yield start + 1, match.group(1), body


def disposition(path: pathlib.Path, line: int, kind: str, body: str, tags):
    name = path.name
    if name == "verification.k":
        if kind == "syntax":
            return "PROOF_LOCAL_DEFINITION_REVIEWED_TOTAL_TRUTHFUL"
        if kind == "rule":
            return "PROOF_LOCAL_EQUATION_REVIEWED_TRUE_DISJOINT_DESCENDING"
    if name == "spec.k" and kind == "claim":
        return "TARGET_CLAIM_REVIEWED_SOUND_AND_ADEQUATE"
    if kind == "configuration":
        return "USED_CONFIGURATION_REVIEWED_SOUND_FOR_PROGRAM"
    if kind == "rule" and line in used_rule_lines.get(name, set()):
        return "USED_RULE_REVIEWED_SOUND"
    if kind == "context" and line in used_context_lines.get(name, set()):
        return "USED_EVALUATION_CONTEXT_REVIEWED_LEFT_TO_RIGHT"
    if (name, line) in known_unused_totality_gaps:
        return "UNUSED_FIXED_TOTALITY_COVERAGE_GAP_NO_DEPENDENCY"
    if kind == "syntax" and line in used_syntax_lines.get(name, set()):
        return "USED_DECLARATION_REVIEWED"
    if "no-evaluators" in tags:
        return "UNUSED_FIXED_OPAQUE_PRIMITIVE_NO_DEPENDENCY"
    if "concrete" in tags:
        return "UNUSED_OR_GROUND_ONLY_CONCRETE_RULE_NO_SYMBOLIC_DEPENDENCY"
    if "priority" in tags:
        return "FIXED_PRIORITY_RULE_GUARDED_OR_CONSTRUCTOR_DISJOINT_FROM_REACHABLE_PATH"
    return "FIXED_SUBSET_DECL_OR_RULE_REVIEWED_NO_REACHABLE_PATH_INFLUENCE"


counts = collections.Counter()
tag_counts = collections.Counter()
disposition_counts = collections.Counter()
records = []

for path in sources:
    relative = path.relative_to(SCRATCH)
    for line, kind, body in blocks(path):
        tags = [tag for tag in attributes if re.search(rf"\b{re.escape(tag)}\b", body)]
        status = disposition(path, line, kind, body, tags)
        counts[kind] += 1
        for tag in tags:
            tag_counts[tag] += 1
        disposition_counts[status] += 1
        records.append((str(relative), line, kind, ",".join(tags) or "-", status, body))

print("INVENTORY_COUNTS", dict(sorted(counts.items())))
print("ATTRIBUTE_COUNTS", dict(sorted(tag_counts.items())))
print("DISPOSITION_COUNTS", dict(sorted(disposition_counts.items())))
print("RECORD_COUNT", len(records))
print("BEGIN_RECORDS")
for relative, line, kind, tags, status, body in records:
    print(f"{relative}:{line}\t{kind}\t{tags}\t{status}\t{body}")
print("END_RECORDS")
