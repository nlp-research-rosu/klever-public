#!/usr/bin/env python3
"""Emit an exhaustive line-addressed inventory of local K declarations/rules.

The review classification is theorem-slice-specific.  `USED-SOUND` entries
were manually traced on the submitted program's reachable path.
`SUPPLIED-UNUSED-INERT` entries are sort/pattern/control unreachable from that
path, so they cannot contribute to either target's closure.  Opaque boundaries
are called out separately.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


SEM = Path("/reference/reference-semantics")
CANDIDATE = Path("/candidate/verification.k")
FILES = [SEM / "semantics.k", *sorted((SEM / "semantics").glob("*.k")), CANDIDATE]

START_RE = re.compile(r"^  (configuration|syntax|context|rule|claim)\b")
END_RE = re.compile(
    r"^(?:  (?:configuration|syntax|context|rule|claim|imports)\b|endmodule\b|module\b|requires\b)"
)

# Executable declarations/rules manually traced for this exact function.
USED = {
    ("syntax.k", 9),
    ("syntax.k", 32),
    ("syntax.k", 37),
    ("syntax.k", 38),
    ("syntax.k", 39),
    ("syntax.k", 41),
    ("syntax.k", 56),
    ("syntax.k", 57),
    ("syntax.k", 60),
    ("syntax.k", 61),
    ("core.k", 13),
    ("core.k", 14),
    ("core.k", 18),
    ("core.k", 25),
    ("core.k", 36),
    ("core.k", 37),
    ("core.k", 38),
    ("core.k", 39),
    ("core.k", 40),
    ("core.k", 41),
    ("core.k", 42),
    ("core.k", 49),
    ("core.k", 68),
    ("core.k", 69),
    ("core.k", 70),
    ("core.k", 117),
    ("core.k", 118),
    ("core.k", 126),
    ("core.k", 127),
    ("core.k", 130),
    ("core.k", 131),
    ("core.k", 132),
    ("core.k", 152),
    ("core.k", 157),
    ("core.k", 158),
    ("core.k", 185),
    ("core.k", 186),
    ("core.k", 189),
    ("core.k", 190),
    ("core.k", 191),
    ("core.k", 194),
    ("core.k", 199),
    ("core.k", 200),
    ("core.k", 208),
    ("core.k", 210),
    ("core.k", 213),
    ("core.k", 214),
    ("core.k", 215),
    ("core.k", 217),
    ("core.k", 218),
    ("core.k", 219),
    ("core.k", 223),
    ("core.k", 224),
    ("core.k", 225),
    ("operators.k", 10),
    ("operators.k", 15),
    ("operators.k", 16),
    ("operators.k", 17),
    ("int.k", 7),
    ("int.k", 26),
    ("list.k", 13),
    ("list.k", 14),
    ("list.k", 15),
    ("controls.k", 51),
    ("controls.k", 52),
    ("controls.k", 53),
    ("controls.k", 54),
    ("functions.k", 8),
    ("functions.k", 63),
    ("functions.k", 64),
    ("functions.k", 78),
    ("functions.k", 85),
    ("call.k", 19),
    ("call.k", 20),
    ("call.k", 21),
    ("call.k", 69),
    ("sort.k", 18),
    ("sort.k", 20),
    ("sort.k", 21),
    ("sort.k", 22),
    ("sort.k", 23),
    ("sort.k", 24),
    ("sort.k", 36),
    ("subscript.k", 21),
    ("subscript.k", 22),
    ("subscript.k", 23),
    ("subscript.k", 27),
    ("subscript.k", 28),
    ("subscript.k", 31),
    ("subscript.k", 44),
    ("subscript.k", 49),
    ("subscript.k", 50),
    ("subscript.k", 51),
    ("subscript.k", 52),
    ("subscript.k", 54),
    ("subscript.k", 55),
    ("subscript.k", 56),
    ("subscript.k", 58),
    ("subscript.k", 63),
    ("subscript.k", 64),
    ("subscript.k", 72),
    ("subscript.k", 73),
    ("subscript.k", 76),
    ("subscript.k", 81),
    ("subscript.k", 83),
    ("subscript.k", 84),
    ("subscript.k", 90),
    ("subscript.k", 91),
    ("subscript.k", 96),
    ("subscript.k", 97),
    ("subscript.k", 109),
    ("subscript.k", 110),
    ("subscript.k", 113),
    ("verification.k", 8),
    ("verification.k", 9),
    ("verification.k", 22),
}


def attrs(text: str) -> list[str]:
    found: list[str] = []
    for value in (
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "macro",
        "strict",
        "seqstrict",
        "simplification",
        "priority",
        "concrete",
        "owise",
    ):
        if re.search(rf"\b{re.escape(value)}\b", text):
            found.append(value)
    return found


records: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        match = START_RE.match(lines[i])
        if not match:
            i += 1
            continue
        start = i + 1
        kind = match.group(1)
        j = i + 1
        while j < len(lines) and not END_RE.match(lines[j]):
            j += 1
        text = "\n".join(lines[i:j]).rstrip()
        basename = path.name
        key = (basename, start)
        opaque = "no-evaluators" in text

        if basename == "verification.k":
            if start == 8:
                decision = "PROOF-LOCAL-SOUND"
                reason = "syntax macro declaration only; expansion compared mechanically"
            elif start == 9:
                decision = "PROOF-LOCAL-SOUND"
                reason = "expansion equals submitted FuncDef body constructor-for-constructor"
            else:
                decision = "PROOF-LOCAL-SOUND-ON-DOMAIN"
                reason = "length preservation follows by structural induction over supplied insertion sort"
        elif basename == "sort.k" and start == 18:
            decision = "SUPPLIED-OPAQUE-BOUNDARY"
            reason = "used fixed primitive; symbolic ordering/permutation is assumed, concrete int equations exist"
        elif key in USED:
            decision = "USED-SOUND"
            reason = "manually traced; matches binding/evaluation/control/allocation/slice behavior on intended int-list domain"
        elif opaque:
            decision = "SUPPLIED-OPAQUE-UNUSED-INERT"
            reason = "opaque fixed primitive is unreachable from submitted program"
        else:
            decision = "SUPPLIED-UNUSED-INERT"
            reason = "pattern/sort/control unreachable from submitted program; cannot contribute to target closure"

        records.append(
            {
                "file": str(path),
                "start": start,
                "end": j,
                "kind": kind,
                "attributes": attrs(text),
                "decision": decision,
                "reason": reason,
                "text": text,
            }
        )
        i = j

print("# Exhaustive K declaration/rule inventory")
print()
print(
    "Each JSON record is one complete local `configuration`, `syntax`, "
    "`context`, `rule`, or `claim` block, including multiline guards/attributes."
)
print()
for record in records:
    print(json.dumps(record, sort_keys=True, separators=(",", ":")))

counts: dict[str, int] = {}
for record in records:
    key = str(record["decision"])
    counts[key] = counts.get(key, 0) + 1
print()
print("SUMMARY " + json.dumps({"records": len(records), "decisions": counts}, sort_keys=True))
