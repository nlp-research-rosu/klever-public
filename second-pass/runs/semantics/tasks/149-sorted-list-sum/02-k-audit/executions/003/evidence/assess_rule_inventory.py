#!/usr/bin/env python3
"""Assign an explicit audit disposition to every inventoried K sentence."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/149-sorted-list-sum")
files = [ROOT / "reference-semantics/semantics.k"]
files += sorted((ROOT / "reference-semantics/semantics").glob("*.k"))
files += [ROOT / "verification.k", ROOT / "spec.k"]
starter = re.compile(r"^  (configuration|syntax|context|rule|claim)\b")

# Source ranges that are on the submitted term's concrete or symbolic path.
relevant_ranges = {
    "reference-semantics/semantics/syntax.k": [(9, 61)],
    "reference-semantics/semantics/core.k": [
        (13, 42), (49, 60), (68, 70), (95, 102), (117, 127),
        (130, 181), (185, 191), (194, 196), (208, 229),
    ],
    "reference-semantics/semantics/iter.k": [(8, 8)],
    "reference-semantics/semantics/operators.k": [(10, 17), (25, 46)],
    "reference-semantics/semantics/int.k": [(9, 20), (26, 27)],
    "reference-semantics/semantics/str.k": [(43, 59)],
    "reference-semantics/semantics/list.k": [(9, 20), (53, 55)],
    "reference-semantics/semantics/tuple.k": [(31, 41)],
    "reference-semantics/semantics/controls.k": [(9, 18), (48, 74), (104, 108)],
    "reference-semantics/semantics/functions.k": [(8, 20), (62, 90)],
    "reference-semantics/semantics/builtins.k": [(17, 26)],
    "reference-semantics/semantics/call.k": [(15, 74)],
    "reference-semantics/semantics/sort.k": [(18, 49), (61, 62)],
    "reference-semantics/semantics/concrete.k": [(20, 59)],
}


def is_relevant(relative: str, line: int) -> bool:
    return any(start <= line <= end for start, end in relevant_ranges.get(relative, []))


def disposition(relative: str, line: int, category: str, text: str) -> tuple[str, str]:
    if relative == "verification.k":
        if category == "rule" and line == 71:
            return (
                "REJECT-UNSOUND",
                "priority bridge erases nonempty-loop target binding and accepts arbitrary CONT; "
                "see bridge-spurious-transition and fixed ground witness",
            )
        return (
            "ACCEPT-PROOF-LOCAL-DEFINITION",
            "constructor datatype, terminating/disjoint evenAppend equations, exact macro, or exact frame summary",
        )
    if relative == "spec.k":
        if line == 9:
            return (
                "REJECT-FIXED-SEMANTICS-CLAIM",
                "same false arbitrary-CONT transition as rejected bridge; closes only because imported rule restates it",
            )
        return (
            "DEPENDENT-TARGET-CLAIM",
            "result-constraining and exact-program-pinned, but closure depends on rejected bridge",
        )
    if "no-evaluators" in text:
        if relative.endswith("/sort.k") and line in {18, 49}:
            return (
                "ACCEPT-CONDITIONAL-OPAQUE-PRIMITIVE",
                "fixed external sorted primitive; theorem states result using the same symbol and needs its named contract",
            )
        return ("UNUSED-OPAQUE-PRIMITIVE", "opaque fixed-semantics symbol is not reached by submitted term")
    if category in {"syntax", "configuration", "context"}:
        if is_relevant(relative, line):
            return ("ACCEPT-RELEVANT-DECLARATION", "well-sorted declaration/configuration/evaluation context used by term")
        return ("UNUSED-DECLARATION", "not reached by submitted constructor term; checked for label/priority interference")
    if "[concrete]" in text:
        if is_relevant(relative, line):
            return (
                "ACCEPT-CONCRETE-REFERENCE-RULE",
                "ground execution equation used only by concrete reconstruction; symbolic theorem does not import concrete module",
            )
        return ("UNUSED-CONCRETE-RULE", "not reached by submitted term")
    if is_relevant(relative, line):
        return (
            "ACCEPT-RELEVANT-FIXED-RULE",
            "matches Python subset operation and preserves the cells/evaluation order used by submitted term",
        )
    return (
        "UNUSED-FIXED-RULE",
        "no matching redex occurs in submitted term or target claims; no false-conclusion witness asserted",
    )


number = 0
counts: dict[str, int] = {}
print("# Per-sentence static dispositions")
for path in files:
    relative = path.relative_to(ROOT).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = starter.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, category) in enumerate(starts):
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = next_start
        for index in range(start + 1, next_start):
            if lines[index].startswith("endmodule"):
                end = index
                break
        text = " ".join(
            line.strip()
            for line in lines[start:end]
            if line.strip() and not line.lstrip().startswith("//")
        )
        number += 1
        decision, reason = disposition(relative, start + 1, category, text)
        counts[decision] = counts.get(decision, 0) + 1
        print(
            f"{number:04d}\t{relative}:{start + 1}-{end}\t{category.upper()}\t"
            f"{decision}\t{reason}"
        )

print(f"TOTAL={number}")
for decision, count in sorted(counts.items()):
    print(f"COUNT {decision}={count}")
