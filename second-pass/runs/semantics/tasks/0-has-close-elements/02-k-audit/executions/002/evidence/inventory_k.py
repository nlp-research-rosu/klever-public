#!/usr/bin/env python3
"""Exhaustive declaration/rule/claim inventory for the audited K sources."""
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

trusted_root = Path("/reference/reference-semantics")
paths = sorted(trusted_root.rglob("*.k"))
paths += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

start_re = re.compile(r"^\s*(configuration|syntax|rule|claim|context)\b")
stop_re = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context|module|endmodule)\b"
)
attr_token_re = re.compile(
    r"(?:\b(?:function|functional|total|no-evaluators|concrete|owise|"
    r"simplification|macro|macro-rec|strict)\b|"
    r"\b(?:seqstrict|strict|priority|symbol)\([^)]*\))"
)

material_files = {
    "semantics.k",
    "semantics/syntax.k",
    "semantics/core.k",
    "semantics/iter.k",
    "semantics/list.k",
    "semantics/float.k",
    "semantics/int.k",
    "semantics/operators.k",
    "semantics/controls.k",
    "semantics/functions.k",
    "semantics/builtins.k",
    "semantics/call.k",
}

unsound_candidate_rules = {
    130: "UNSOUND_OPERATIONAL_BRIDGE: arbitrary inner-loop body and arbitrary continuation/state frame",
    151: "UNSOUND_OPERATIONAL_BRIDGE: textual helper call without binding or callee-body pinning",
    178: "UNSOUND_OPERATIONAL_BRIDGE: arbitrary outer-loop body and arbitrary continuation/state frame",
    197: "UNSOUND_OPERATIONAL_BRIDGE: textual entry call without binding or callee-body pinning",
}

candidate_rule_roles = {
    8: "exact body constructor definition",
    19: "exact body constructor definition",
    27: "exact body constructor definition",
    38: "exact body constructor definition",
    50: "exact body constructor definition",
    62: "exact closure definition",
    64: "exact closure definition",
    68: "exact module constructor definition",
    80: "exact module-scope definition",
    91: "typed-list iterator bridge: empty",
    93: "typed-list iterator bridge: cons",
    98: "pair-distance summary definition",
    103: "closeSkip base equation",
    104: "closeSkip skipped-prefix recursion",
    108: "closeSkip compared-suffix recursion",
    117: "hasPairs base equation",
    118: "hasPairs recursion",
}

rows: list[dict[str, str | int]] = []
for path in paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if start_re.match(line)]
    for index, start in enumerate(starts):
        match = start_re.match(lines[start])
        assert match is not None
        kind = match.group(1)
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        # Do not absorb an intervening module boundary into the declaration.
        for probe in range(start + 1, end):
            if re.match(r"^\s*(module|endmodule)\b", lines[probe]):
                end = probe
                break
        block = "\n".join(lines[start:end]).strip()
        normalized = re.sub(r"\s+", " ", block)
        attrs = ";".join(dict.fromkeys(attr_token_re.findall(block)))
        if path.is_relative_to(trusted_root):
            rel = str(path.relative_to(trusted_root))
            source_class = "SUPPLIED_FIXED_SEMANTICS"
            materiality = (
                "TARGET_PATH_OR_SUPPORT_MODULE"
                if rel in material_files
                else "UNUSED_BY_SUBMITTED_PROGRAM"
            )
            assessment = (
                "ACCEPTED_SELECTED_SEMANTICS; no target-path false-rule witness found"
                if materiality == "TARGET_PATH_OR_SUPPORT_MODULE"
                else "OUTSIDE_TARGET_PATH; cannot contribute to this proof execution"
            )
        elif path.name == "verification.k":
            rel = "verification.k"
            source_class = "CANDIDATE_PROOF_EXTENSION"
            materiality = "TARGET_PROOF_THEORY"
            if kind == "rule" and start + 1 in unsound_candidate_rules:
                assessment = unsound_candidate_rules[start + 1]
            elif kind == "rule" and start + 1 == 163:
                assessment = (
                    "UNJUSTIFIED_OR_DEAD_OPERATIONAL_BRIDGE: arbitrary closure "
                    "body; attempted witness did not match, so no unsoundness label"
                )
            elif kind == "rule":
                role = candidate_rule_roles.get(start + 1, "declaration-supporting equation")
                assessment = f"ACCEPTED_LOCALLY: {role}"
            else:
                assessment = "DECLARATION; checked with its defining rules"
        else:
            rel = "spec.k"
            source_class = "CANDIDATE_CLAIM"
            materiality = "PROOF_OBLIGATION"
            assessment = (
                "CLAIM_ONLY; independently rebuilt (not treated as an axiom)"
                if kind == "claim"
                else "DECLARATION/CONTEXT"
            )
        rows.append(
            {
                "id": len(rows) + 1,
                "source": rel,
                "line": start + 1,
                "kind": kind,
                "attributes": attrs,
                "source_class": source_class,
                "materiality": materiality,
                "assessment": assessment,
                "normalized_declaration": normalized,
            }
        )

out = Path("/audit-output/evidence/05-rule-inventory.tsv")
with out.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

kind_counts = Counter(str(row["kind"]) for row in rows)
class_counts = Counter(str(row["source_class"]) for row in rows)
assessment_counts = Counter(
    "UNSOUND"
    if str(row["assessment"]).startswith("UNSOUND")
    else "CLAIM"
    if row["source_class"] == "CANDIDATE_CLAIM"
    else "ACCEPTED_OR_DECLARATION"
    for row in rows
)
attr_counts = Counter()
for row in rows:
    for attr in str(row["attributes"]).split(";"):
        if attr:
            attr_counts[attr] += 1

summary = Path("/audit-output/evidence/05-rule-inventory-summary.txt")
with summary.open("w", encoding="utf-8") as handle:
    handle.write(f"inventory_entries={len(rows)}\n")
    handle.write("kind_counts=" + repr(dict(sorted(kind_counts.items()))) + "\n")
    handle.write("source_class_counts=" + repr(dict(sorted(class_counts.items()))) + "\n")
    handle.write("assessment_counts=" + repr(dict(sorted(assessment_counts.items()))) + "\n")
    handle.write("attribute_counts=" + repr(dict(sorted(attr_counts.items()))) + "\n")
    handle.write("unsound_candidate_entries:\n")
    for row in rows:
        if str(row["assessment"]).startswith("UNSOUND"):
            handle.write(
                f"  {row['source']}:{row['line']} {row['assessment']}\n"
            )

print(summary.read_text(encoding="utf-8"), end="")
