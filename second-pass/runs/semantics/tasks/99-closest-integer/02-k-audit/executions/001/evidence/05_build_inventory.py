#!/usr/bin/env python3
"""Build a complete top-level K declaration/rule inventory for the audit."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/99-closest-integer-audit/candidate")
OUT = Path("/audit-output/evidence")
START = re.compile(
    r"^(?:(requires)\b|\s{0,2}(module|imports|configuration|syntax|rule|context|claim|endmodule)\b)"
)
ATTR = re.compile(r"\[([^\]]+)\]")
K_ATTRIBUTE = re.compile(
    r"\b(function|total|functional|simplification|concrete|owise|"
    r"no-evaluators|macro|macro-rec|strict|seqstrict|priority|symbol)\b"
)

# Blocks that participate in execution of this submitted algorithm, either in
# the symbolic target harness or in concrete execution of solution.mpy.
SLICE_RANGES = {
    "reference-semantics/semantics.k": [(34, 90)],
    "reference-semantics/semantics/syntax.k": [
        (9, 16), (28, 32), (41, 41), (49, 50), (53, 53), (56, 61)
    ],
    "reference-semantics/semantics/core.k": [
        (13, 16), (25, 43), (49, 60), (124, 127), (130, 181),
        (183, 191), (199, 215)
    ],
    "reference-semantics/semantics/functions.k": [
        (8, 20), (62, 90)
    ],
    "reference-semantics/semantics/call.k": [
        (18, 32), (69, 75)
    ],
    "reference-semantics/semantics/controls.k": [
        (8, 18), (50, 54)
    ],
    "reference-semantics/semantics/operators.k": [
        (12, 17)
    ],
    "reference-semantics/semantics/float.k": [
        (19, 21), (101, 113), (123, 127), (157, 187), (208, 214)
    ],
    "reference-semantics/semantics/str.k": [(12, 17)],
    "reference-semantics/semantics/builtins.k": [(14, 17)],
    "reference-semantics/semantics/assert.k": [(6, 16)],
    "verification.k": [(1, 35)],
    "spec.k": [(1, 25)],
}


def in_slice(source: str, start: int, end: int) -> bool:
    return any(
        start <= range_end and end >= range_start
        for range_start, range_end in SLICE_RANGES.get(source, [])
    )


def decision(source: str, start: int, kind: str, text: str, used: bool) -> str:
    if source == "verification.k":
        if kind == "rule" and start == 21:
            return "PROOF_LOCAL_IDENTITY_GAP: wrapper executes copied closestBody, not solution.mpy"
        if kind == "rule" and start == 30:
            return "PROOF_LOCAL_STRUCTURAL_SPEC: truthful equation, but not an independent nearest-integer theorem"
        if kind == "rule" and start == 10:
            return "PROOF_LOCAL_COPIED_BODY: exact current syntax, but no formal source dependency"
        return "PROOF_LOCAL_DECLARATION_REVIEWED"
    if source == "spec.k":
        if kind == "claim":
            return "TARGET_CLAIM: closes structurally; fails real-program pinning and intent adequacy"
        return "SPEC_DECLARATION_REVIEWED"
    if "no-evaluators" in text:
        prefix = "USED_" if used else "UNUSED_"
        return prefix + "FIXED_SUPPLIED_OPAQUE_BOUNDARY"
    if "[concrete]" in text:
        prefix = "USED_" if used else "UNUSED_"
        return prefix + "FIXED_SUPPLIED_CONCRETE_RULE"
    if "priority(" in text:
        prefix = "USED_" if used else "UNUSED_"
        return prefix + "FIXED_SUPPLIED_PRIORITY_RULE"
    if used:
        return "USED_FIXED_SUPPLIED_SEMANTICS"
    return "UNUSED_FIXED_SUPPLIED_SEMANTICS"


paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
paths.extend([ROOT / "verification.k", ROOT / "spec.k"])
records = []

for path in paths:
    source = str(path.relative_to(ROOT))
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines, start=1):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for position, (start, kind) in enumerate(starts):
        end = (starts[position + 1][0] - 1) if position + 1 < len(starts) else len(lines)
        numbered_block = [
            (line_number, lines[line_number - 1])
            for line_number in range(start, end + 1)
            if lines[line_number - 1].strip()
            and not lines[line_number - 1].lstrip().startswith("//")
        ]
        while numbered_block and not numbered_block[-1][1].strip():
            numbered_block.pop()
        end = numbered_block[-1][0] if numbered_block else start
        text = " ".join(line.strip() for _, line in numbered_block)
        attributes = [
            attr_group.strip()
            for attr_group in ATTR.findall(text)
            if K_ATTRIBUTE.search(attr_group)
        ]
        used = in_slice(source, start, end)
        records.append(
            {
                "id": len(records) + 1,
                "source": source,
                "start_line": start,
                "end_line": end,
                "kind": kind,
                "attributes": attributes,
                "program_slice": used,
                "decision": decision(source, start, kind, text, used),
                "text": text,
            }
        )

(OUT / "05_rule_inventory.json").write_text(
    json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

counts: dict[str, int] = {}
decisions: dict[str, int] = {}
for record in records:
    counts[record["kind"]] = counts.get(record["kind"], 0) + 1
    decisions[record["decision"]] = decisions.get(record["decision"], 0) + 1

with (OUT / "05_rule_inventory.md").open("w", encoding="utf-8") as output:
    output.write("# Exhaustive K declaration and rule inventory\n\n")
    output.write(
        "This inventory is mechanically extracted from the fresh scratch copy. "
        "Every top-level `requires`, module/import, configuration, syntax block, "
        "context, rule, and claim is listed. The exact unabridged records are also "
        "available in `05_rule_inventory.json`.\n\n"
    )
    output.write(f"Total records: {len(records)}\n\n")
    output.write("Kinds: `" + json.dumps(counts, sort_keys=True) + "`\n\n")
    output.write("Decision counts:\n\n")
    for label, count in sorted(decisions.items()):
        output.write(f"- `{label}`: {count}\n")
    output.write("\n")
    output.write("| ID | Source | Lines | Kind | Attributes | Slice | Decision | Declaration/rule |\n")
    output.write("|---:|---|---:|---|---|---|---|---|\n")
    for record in records:
        escaped = (
            record["text"]
            .replace("&", "&amp;")
            .replace("|", "&#124;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        attrs = ", ".join(record["attributes"]).replace("|", "&#124;")
        decision_text = record["decision"].replace("|", "&#124;")
        output.write(
            f"| {record['id']} | `{record['source']}` | "
            f"{record['start_line']}-{record['end_line']} | `{record['kind']}` | "
            f"{attrs} | {'yes' if record['program_slice'] else 'no'} | "
            f"{decision_text} | {escaped} |\n"
        )

print(f"inventory records: {len(records)}")
print("kind counts:", json.dumps(counts, sort_keys=True))
print("decision counts:", json.dumps(decisions, sort_keys=True))
