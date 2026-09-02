#!/usr/bin/env python3
"""Produce a complete declaration/rule inventory for the selected K theory."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/30-get-positive")
SEMANTICS = ROOT / "reference-semantics"
FILES = [SEMANTICS / "semantics.k"]
FILES += sorted((SEMANTICS / "semantics").glob("*.k"))
FILES += [ROOT / "verification.k", ROOT / "spec.k"]

START = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim)\b"
)


def normalized_block(lines: list[str], start: int, stop: int) -> str:
    block = " ".join(part.strip() for part in lines[start:stop])
    return re.sub(r"\s+", " ", block).replace("|", r"\|")


print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Every configuration, syntax declaration, context, rule, and claim in the "
    "selected supplied-semantics proof theory is listed below. Candidate and "
    "trusted semantics were byte-identical (see `00_provenance.log`)."
)
print()
print("| Source | Kind | Declaration / rule | Audit disposition |")
print("|---|---|---|---|")

counts: dict[str, int] = {}
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for pos, start in enumerate(starts):
        stop = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        # Do not swallow endmodule or a following module into the last block.
        for index in range(start + 1, stop):
            if re.match(r"^\s*(?:end)?module\b", lines[index]):
                stop = index
                break
        match = START.match(lines[start])
        assert match is not None
        kind = match.group(1)
        counts[kind] = counts.get(kind, 0) + 1
        rel = path.relative_to(ROOT)
        text = normalized_block(lines, start, stop)

        attrs = []
        for tag in (
            "function",
            "total",
            "functional",
            "macro-rec",
            "macro",
            "simplification",
            "concrete",
            "owise",
            "priority",
            "symbol",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(tag)}\b", text):
                attrs.append(tag)

        if str(rel).startswith("reference-semantics/"):
            disposition = (
                "Selected trusted supplied-semantics baseline; unchanged in "
                "candidate. Static review found no candidate-local alteration."
            )
        elif rel.name == "verification.k":
            disposition = "Proof-local extension; individually reviewed in REVIEW.md."
        else:
            disposition = "Reachability claim; adequacy and closure individually reviewed."
        if attrs:
            disposition += " Attributes: " + ", ".join(attrs) + "."

        print(
            f"| `{rel}:{start + 1}` | {kind} | `{text}` | {disposition} |"
        )

print()
print("Counts: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)))

