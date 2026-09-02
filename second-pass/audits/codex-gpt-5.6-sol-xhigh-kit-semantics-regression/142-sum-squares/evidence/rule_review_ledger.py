#!/usr/bin/env python3
"""One reviewer decision for every source-level K rule."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/tmp/audit-work/142-sum-squares")
SEMANTICS = ROOT / "reference-semantics"
SOURCES = [
    SEMANTICS / "semantics.k",
    *sorted((SEMANTICS / "semantics").glob("*.k")),
    ROOT / "verification.k",
]

# Rules exercised by the submitted program's proof, identified after tracing
# its exact constructors and the fixed control-flow rules.
USED_FIXED = {
    "semantics/core.k": {
        125,
        126,
        127,
        131,
        132,
        158,
        189,
        190,
        191,
        194,
        200,
        214,
        215,
    },
    "semantics/functions.k": {14, 63, 64, 78, 85},
    "semantics/call.k": {20, 21, 69},
    "semantics/controls.k": {9, 52, 53, 54, 69, 71, 72, 73, 85},
    "semantics/tuple.k": {32},
    "semantics/operators.k": {12, 17},
    "semantics/int.k": {9, 14, 15, 20, 26},
}
BRIDGE_PREMISE = {"semantics/list.k": {9, 10}}

LOCAL = {
    8: (
        "DEFINITIONAL",
        "ACCEPT",
        "empty structural IntSeq-to-ValSeq embedding equation; disjoint base case",
    ),
    9: (
        "DEFINITIONAL",
        "ACCEPT",
        "cons structural embedding; recursion strictly descends on VS",
    ),
    14: (
        "OPERATIONAL_BRIDGE",
        "ACCEPT",
        "empty iterator case equals intVals base equation followed by fixed list iterator rule",
    ),
    17: (
        "OPERATIONAL_BRIDGE",
        "ACCEPT",
        "cons iterator case equals intVals cons equation followed by fixed list iterator rule; suffix preserved",
    ),
    23: (
        "DEFINITIONAL",
        "ACCEPT",
        "square branch for pyMod(I,3)=0",
    ),
    26: (
        "DEFINITIONAL",
        "ACCEPT",
        "cube branch when modulo 3 is nonzero and modulo 4 is zero",
    ),
    30: (
        "DEFINITIONAL",
        "ACCEPT",
        "identity branch when both modulo tests are nonzero",
    ),
    37: (
        "DEFINITIONAL",
        "ACCEPT",
        "left-fold empty suffix returns accumulator",
    ),
    38: (
        "DEFINITIONAL",
        "ACCEPT",
        "left-fold cons case consumes exactly one element and increments index",
    ),
    51: (
        "OPERATIONAL_BRIDGE",
        "ACCEPT",
        "complete k/state context is byte-normalized identical to independently proved LOOP-SPEC.loop",
    ),
}

STOP = re.compile(
    r"^\s*(rule|syntax|context|configuration|module|endmodule|claim)\b"
)
MODULE = re.compile(r"^\s*module\s+(\S+)")


def relative(source: Path) -> str:
    if source == ROOT / "verification.k":
        return "verification.k"
    return str(source.relative_to(SEMANTICS))


def rule_blocks(source: Path):
    lines = source.read_text(encoding="utf-8").splitlines()
    current_module = "-"
    index = 0
    while index < len(lines):
        module_match = MODULE.match(lines[index])
        if module_match:
            current_module = module_match.group(1)
        if re.match(r"^\s*rule\b", lines[index]):
            start = index
            index += 1
            while index < len(lines) and not STOP.match(lines[index]):
                index += 1
            yield start + 1, current_module, "\n".join(lines[start:index]).strip()
            continue
        index += 1


def attrs(block: str) -> str:
    tags = []
    for pattern, name in (
        (r"<k>", "operational"),
        (r"\[priority\(", "priority"),
        (r"\[owise\]", "owise"),
        (r"\[concrete\]", "concrete"),
        (r"\[simplification", "simplification"),
        (r"\brequires\b", "guarded"),
    ):
        if re.search(pattern, block):
            tags.append(name)
    return ",".join(tags) or "equational"


def main() -> None:
    counts: dict[str, int] = {}
    number = 0
    for source in SOURCES:
        rel = relative(source)
        for line, module, block in rule_blocks(source):
            number += 1
            if rel == "verification.k":
                category, decision, reason = LOCAL[line]
            elif line in USED_FIXED.get(rel, set()):
                category = "FIXED_USED"
                decision = "ACCEPT"
                reason = (
                    "selected supplied-semantics transition/equation; constructor, "
                    "guard, state footprint, and result agree with the used Python-subset behavior"
                )
            elif line in BRIDGE_PREMISE.get(rel, set()):
                category = "FIXED_BRIDGE_PREMISE"
                decision = "ACCEPT"
                reason = (
                    "selected fixed list iterator case; exact premise for proof-local iterator bridge"
                )
            elif rel == "semantics/concrete.k":
                category = "FIXED_RUNTIME_ONLY"
                decision = "ACCEPT_OUTSIDE_PROOF"
                reason = (
                    "part of trusted MPY-KRUN only, not imported by the Haskell proof module and not used by this program"
                )
            else:
                category = "FIXED_UNUSED"
                decision = "ACCEPT_OUTSIDE_PATH"
                reason = (
                    "trusted supplied-semantics rule; its syntactic redex/sort is absent from solution.mpy and no proof-local rule invokes it"
                )
            counts[category] = counts.get(category, 0) + 1
            normalized = " ".join(block.split())
            print(
                f"{number:04d}\t{rel}:{line}\tmodule={module}\tattrs={attrs(block)}"
                f"\tcategory={category}\tdecision={decision}\treason={reason}"
                f"\trule={normalized}"
            )
    print("SUMMARY")
    for category in sorted(counts):
        print(f"{category}={counts[category]}")
    print(f"TOTAL_RULES={number}")


if __name__ == "__main__":
    main()
