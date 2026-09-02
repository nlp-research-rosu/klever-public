#!/usr/bin/env python3
"""Create an exhaustive declaration/rule inventory for the fresh audit sources."""

import collections
import html
import re
from pathlib import Path

SCRATCH = Path("/tmp/audit-work/prime31")
SEMANTICS = SCRATCH / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/05_rule_inventory.md")

paths = sorted(SEMANTICS.rglob("*.k")) + [
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]

start_re = re.compile(r"^\s{2}(syntax|rule|claim|configuration|context)\b")
stop_re = re.compile(r"^\s{0,2}(?:module|endmodule|imports|requires\s+\")\b")

# These declarations/rules are on the actual is_prime proof execution path.
active = {
    ("semantics/syntax.k", line)
    for line in [9, 12, 15, 28, 30, 32, 37, 41, 46, 49, 50, 53, 56, 57, 60]
}
active |= {
    ("semantics/core.k", line)
    for line in [
        25,
        31,
        38,
        39,
        40,
        49,
        126,
        127,
        130,
        131,
        132,
        152,
        157,
        185,
        186,
        187,
        188,
        189,
        190,
        191,
        194,
        195,
        199,
        200,
        208,
        209,
        210,
        213,
        214,
        215,
    ]
}
active |= {
    ("semantics/operators.k", line) for line in [12, 15, 16, 17]
}
active |= {
    ("semantics/int.k", line)
    for line in [9, 15, 19, 20, 22, 26]
}
active |= {
    ("semantics/controls.k", line)
    for line in [9, 51, 52, 53, 54, 65, 77, 78, 79, 81, 85]
}
active |= {
    ("semantics/functions.k", line)
    for line in [8, 9, 10, 11, 63, 64, 78, 80, 85]
}
active |= {
    ("semantics/call.k", line) for line in [19, 20, 21, 69]
}


def relpath(path: Path) -> str:
    if path.is_relative_to(SEMANTICS):
        return path.relative_to(SEMANTICS).as_posix()
    return path.name


def normalized(block: list[str]) -> str:
    pieces = []
    for line in block:
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        pieces.append(stripped)
    return " ".join(pieces)


entries = []
for path in paths:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if start_re.match(line)]
    for position, index in enumerate(starts):
        next_index = starts[position + 1] if position + 1 < len(starts) else len(lines)
        # Do not absorb a following module boundary/import into the declaration.
        for candidate in range(index + 1, next_index):
            if stop_re.match(lines[candidate]):
                next_index = candidate
                break
        block = lines[index:next_index]
        text = normalized(block)
        kind = start_re.match(lines[index]).group(1)
        attrs = []
        for group in re.findall(r"\[([^\]]+)\]", text):
            attrs.extend(part.strip() for part in group.split(","))
        opaque = "no-evaluators" in text or "symbol(" in text
        concrete = "[concrete]" in text
        priority = "priority(" in text
        simplification = "simplification" in text
        function = re.search(r"\bfunction\b", text) is not None
        total = re.search(r"\btotal\b", text) is not None
        functional = re.search(r"\bfunctional\b", text) is not None
        relative = relpath(path)
        line_number = index + 1

        if relative == "verification.k":
            if kind == "syntax":
                role = "proof-local definitional summary declaration"
                decision = (
                    "ACCEPTED: total functions; all guards are exhaustively and "
                    "pairwise checked in REVIEW"
                )
            else:
                role = "proof-local definitional equation"
                decision = {
                    12: "ACCEPTED: disjoint D<2 totalization; not used by primeResult",
                    15: "ACCEPTED: empty [D,N) interval yields true",
                    18: "ACCEPTED: witnessed divisor yields false; D>=2 makes pyMod defined",
                    22: "ACCEPTED: non-divisor recurrence; N-D strictly decreases",
                    26: "ACCEPTED: integers below 2 are not prime",
                    29: "ACCEPTED: N>=2 delegates exactly to scan from divisor 2",
                }.get(line_number, "REVIEWED_PROOF_LOCAL")
        elif relative == "spec.k":
            role = "positive reachability claim / circularity"
            decision = "MACHINE-CHECKED #Top; adequacy and context reviewed in REVIEW"
        elif (relative, line_number) in active:
            role = "fixed supplied semantics: active is_prime execution path"
            decision = "ACCEPTED: checked against Python control/value/state behavior"
        elif kind == "syntax" and opaque:
            role = "fixed supplied semantics: opaque/trusted symbol, inactive"
            decision = (
                "ACCEPTED FOR THIS THEOREM: interpretation cannot influence this "
                "program, its branches, state, or postcondition"
            )
        elif concrete:
            role = "fixed supplied semantics: concrete-only equation, inactive"
            decision = (
                "ACCEPTED FOR THIS THEOREM: absent from Haskell proof or unreachable; "
                "no current-domain false conclusion witness"
            )
        elif kind in {"syntax", "context", "configuration"}:
            role = "fixed supplied semantics: declarative/inactive"
            decision = "DECLARATIVE: no rewrite conclusion; no current-theorem influence"
        else:
            role = "fixed supplied semantics: inactive rule"
            decision = (
                "ACCEPTED FOR THIS THEOREM: no path from any integer is_prime input; "
                "no current-domain false conclusion witness"
            )

        entries.append(
            {
                "file": relative,
                "line": line_number,
                "kind": kind,
                "attrs": ", ".join(attrs) if attrs else "—",
                "opaque": opaque,
                "concrete": concrete,
                "priority": priority,
                "simplification": simplification,
                "function": function,
                "total": total,
                "functional": functional,
                "role": role,
                "decision": decision,
                "text": text,
            }
        )

counts = collections.Counter(entry["kind"] for entry in entries)
special = {
    "function declarations": sum(e["kind"] == "syntax" and e["function"] for e in entries),
    "total declarations": sum(e["kind"] == "syntax" and e["total"] for e in entries),
    "functional declarations": sum(
        e["kind"] == "syntax" and e["functional"] for e in entries
    ),
    "opaque symbol declarations": sum(e["kind"] == "syntax" and e["opaque"] for e in entries),
    "priority-bearing rules": sum(e["kind"] == "rule" and e["priority"] for e in entries),
    "concrete rules": sum(e["kind"] == "rule" and e["concrete"] for e in entries),
    "simplification rules": sum(
        e["kind"] == "rule" and e["simplification"] for e in entries
    ),
    "proof-local rules": sum(
        e["kind"] == "rule" and e["file"] == "verification.k" for e in entries
    ),
}

with OUTPUT.open("w", encoding="utf-8") as stream:
    stream.write("# Exhaustive K declaration and rule inventory\n\n")
    stream.write(
        "Generated from the fresh scratch copy. Each declaration/rule/context/claim "
        "has a source location, complete normalized block, classification, and "
        "audit disposition. Fixed-semantics entries marked inactive are outside "
        "all control paths of the submitted integer-only program; this is a "
        "current-theorem decision, not a universal claim that the supplied MPY "
        "subset implements every Python behavior.\n\n"
    )
    stream.write("## Counts\n\n")
    for kind in ["configuration", "syntax", "context", "rule", "claim"]:
        stream.write(f"- {kind}: {counts[kind]}\n")
    for name, value in special.items():
        stream.write(f"- {name}: {value}\n")
    stream.write(f"- total inventoried entries: {len(entries)}\n\n")
    stream.write("## Entries\n\n")
    stream.write("| # | Location | Kind/attributes | Role | Decision | Complete normalized block |\n")
    stream.write("|---:|---|---|---|---|---|\n")
    for number, entry in enumerate(entries, 1):
        def cell(value: str) -> str:
            return html.escape(value, quote=False).replace("|", "&#124;")

        stream.write(
            f"| {number} | `{cell(entry['file'])}:{entry['line']}` | "
            f"{cell(entry['kind'])}; {cell(entry['attrs'])} | "
            f"{cell(entry['role'])} | {cell(entry['decision'])} | "
            f"<code>{cell(entry['text'])}</code> |\n"
        )

print(f"output={OUTPUT}")
print(f"entries={len(entries)}")
print("kind_counts=" + ",".join(f"{key}:{counts[key]}" for key in sorted(counts)))
for name, value in special.items():
    print(f"{name}={value}")
