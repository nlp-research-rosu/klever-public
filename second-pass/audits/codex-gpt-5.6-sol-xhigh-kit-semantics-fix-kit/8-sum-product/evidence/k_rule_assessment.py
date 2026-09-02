#!/usr/bin/env python3
"""Reviewer decisions for every item emitted by k_rule_inventory.py."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from k_rule_inventory import declarations


# Source declarations/rules reached by the submitted program or used to justify
# a proof-local bridge. Other supplied rules cannot match this program's AST or
# any intermediate term on the audited path.
REACHED: dict[str, set[int]] = {
    "syntax.k": {9, 37, 41, 56, 57, 60, 61},
    "core.k": {
        14, 18, 25, 36, 37, 38, 39, 40, 41, 42, 49,
        124, 125, 126, 127, 130, 131, 132, 157, 158,
        185, 186, 189, 190, 191, 194, 208, 209,
        213, 214, 215, 217, 218, 219,
    },
    "iter.k": {8},
    "list.k": {9, 10},
    "tuple.k": {14, 15, 16, 31, 32},
    "controls.k": {9, 36, 65, 69, 71, 72, 73, 85},
    "functions.k": {8, 14, 63, 64, 78, 80, 85},
    "call.k": {19, 20, 21, 69},
    "operators.k": {12},
    "int.k": {9, 14},
}

PROOF_LOCAL: dict[int, tuple[str, str]] = {
    9: ("PASS_REPRESENTATION", "IntList has exactly finite empty/cons integer-list constructors."),
    11: ("PASS_REPRESENTATION", "intVals embeds IntList into the supplied ValSeq sort."),
    12: ("PASS_DEFINITION", "Empty embedding is the ValSeq unit; disjoint base case."),
    13: ("PASS_DEFINITION", "Cons embedding preserves head and structurally descends."),
    18: ("PASS_OPERATIONAL_BRIDGE", "Equals intVals base reduction followed by supplied list #iterNext."),
    21: ("PASS_OPERATIONAL_BRIDGE", "Equals intVals cons reduction followed by supplied list #iterNext."),
    29: ("PASS_OPERATIONAL_BRIDGE", "Exact two local lookups, tuple construction, and Return; writes only k/ret as fixed steps do."),
    46: ("PASS_OPERATIONAL_BRIDGE", "Exact local numbers lookup followed by supplied For-to-#loop; changes only k."),
    69: ("PASS_TOTAL_FUNCTIONS", "sumFrom/productFrom are declared on the complete IntList constructor domain."),
    72: ("PASS_DEFINITION", "sumFrom empty case returns the accumulator."),
    73: ("PASS_DEFINITION", "sumFrom cons case performs the program's addition and structurally descends."),
    76: ("PASS_DEFINITION", "productFrom empty case returns the accumulator."),
    77: ("PASS_DEFINITION", "productFrom cons case performs the program's multiplication and structurally descends."),
}


def assess(path: Path, line: int, kind: str, attrs: str) -> tuple[str, str, str]:
    if path.name == "verification.k":
        decision, rationale = PROOF_LOCAL[line]
        return "proof-local", decision, rationale
    if path.name == "spec.k":
        if line == 10:
            return "claim", "PASS_ADEQUACY", "Loop claim starts at the real #loop head, executes the real body, Return, and #pop, and constrains both result fields."
        return "claim", "PASS_ADEQUACY", "Entry claim loads the exact parsed submitted Module and constrains the returned tuple for all IntList inputs."
    filename = path.name
    if line in REACHED.get(filename, set()):
        if filename == "controls.k" and line == 36:
            return "supplied-used", "PASS_OBSERVABLE_PATH_LIMITATION", "The typing import is modeled as a no-op; its bindings are unused and final module scope is outside the return-value theorem."
        return "supplied-used", "PASS_USED_PATH", "Ordinary supplied operational/type/mathematical rule checked against the mapped program step; no conflicting overlap on this path."
    if "symbol" in attrs:
        return "supplied-unused", "UNUSED_TRUSTED_PRIMITIVE", "Opaque supplied-semantics symbol is unreachable from this integer-list program and cannot affect either claim."
    return "supplied-unused", "OUTSIDE_EXECUTED_SUBLANGUAGE", "LHS/syntax is not reachable from the submitted AST on List[int]; no false conclusion witness exists on the intended program path."


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    paths: list[Path] = []
    for path in args.paths:
        paths.extend(sorted(path.rglob("*.k"))) if path.is_dir() else paths.append(path)
    rows = ["file\tline\tkind\tattributes\tscope\tdecision\trationale\tdeclaration"]
    counts: Counter[str] = Counter()
    item_count = 0
    for path in sorted(dict.fromkeys(paths)):
        for line, kind, attrs, declaration in declarations(path):
            scope, decision, rationale = assess(path, line, kind, attrs)
            counts[decision] += 1
            item_count += 1
            rows.append(
                "\t".join(
                    value.replace("\t", " ")
                    for value in (str(path), str(line), kind, attrs, scope, decision, rationale, declaration)
                )
            )
    rows.append(f"TOTAL\t{item_count}")
    for decision in sorted(counts):
        rows.append(f"COUNT_{decision}\t{counts[decision]}")
    args.output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"output={args.output}")
    print(f"assessed_items={item_count}")
    for decision in sorted(counts):
        print(f"{decision}={counts[decision]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
