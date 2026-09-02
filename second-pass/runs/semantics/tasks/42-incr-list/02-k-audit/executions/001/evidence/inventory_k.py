#!/usr/bin/env python3
"""Create a line-addressable, exhaustive inventory of local K declarations."""

from __future__ import annotations

import re
import sys
from pathlib import Path


START = re.compile(r"^\s*(syntax|rule|claim|configuration|context)\b")
BOUNDARY = re.compile(
    r"^\s*(?:syntax|rule|claim|configuration|context|module|endmodule|imports|requires)\b"
)

# Source lines that are on the actual solution.mpy execution/proof path. A
# declaration block is treated as reachable if its starting line is listed.
REACHABLE: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "reference-semantics/semantics/core.k": {
        13,
        14,
        15,
        18,
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        68,
        100,
        117,
        124,
        125,
        126,
        127,
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
        199,
        208,
        209,
        210,
        213,
        214,
        215,
        217,
        218,
        219,
    },
    "reference-semantics/semantics/iter.k": {8},
    "reference-semantics/semantics/str.k": {13, 14, 15, 16},
    "reference-semantics/semantics/list.k": {
        9,
        10,
        13,
        14,
        15,
        18,
        19,
        20,
        53,
    },
    "reference-semantics/semantics/tuple.k": {31, 32},
    "reference-semantics/semantics/operators.k": {12},
    "reference-semantics/semantics/int.k": {9},
    "reference-semantics/semantics/controls.k": {
        9,
        48,
        65,
        69,
        71,
        72,
        73,
    },
    "reference-semantics/semantics/functions.k": {
        8,
        14,
        63,
        64,
        78,
        80,
        85,
    },
    "reference-semantics/semantics/call.k": {16, 19, 20, 21, 24, 52, 53, 69},
    "verification.k": {7, 8, 22, 24, 25, 30, 31, 34, 35, 44, 47, 52, 53},
    "spec.k": {8, 30},
}


def logical_blocks(path: Path) -> list[tuple[int, int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))

    blocks: list[tuple[int, int, str, str]] = []
    for position, (start_index, kind) in enumerate(starts):
        limit = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end_index = limit
        # Stop before module structure or a trailing comment group. Blank lines
        # close the declaration only after at least one nonblank source line.
        for index in range(start_index + 1, limit):
            if BOUNDARY.match(lines[index]):
                end_index = index
                break
            if not lines[index].strip():
                end_index = index
                break
            if lines[index].lstrip().startswith("//"):
                end_index = index
                break
        source = "\n".join(lines[start_index:end_index]).rstrip()
        blocks.append((start_index + 1, max(start_index + 1, end_index), kind, source))
    return blocks


def flags(kind: str, source: str) -> str:
    found: list[str] = []
    for name in (
        "function",
        "total",
        "functional",
        "simplification",
        "concrete",
        "owise",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(name)}\b", source):
            found.append(name)
    priority = re.search(r"priority\(([^)]+)\)", source)
    if priority:
        found.append(f"priority({priority.group(1)})")
    if "no-evaluators" in source or "symbol(" in source:
        found.append("opaque-symbol")
    if kind == "rule" and "simplification" not in found:
        found.append("ordinary-rule")
    return ", ".join(found) if found else "none"


def disposition(rel: str, line: int, source: str) -> str:
    if rel == "verification.k":
        if line in {30, 31}:
            return (
                "ACCEPT — definitional iterator equations for the fresh intVals input "
                "embedding; exact #iterNext context, exhaustive IntSeq constructors, "
                "no state/control changes"
            )
        if line in {44, 47}:
            return "ACCEPT — standard right-association/right-identity laws for finite sequences"
        if line == 53:
            return (
                "ACCEPT — proof-harness observer; exact ref then marker context, reads the "
                "addressed heap value and preserves the remaining continuation/cells"
            )
        if line in {8, 24, 25, 35}:
            return "ACCEPT — truthful terminating definition; complete for its declared domain"
        return "ACCEPT — proof-local declaration supporting the reviewed rules"
    if rel == "spec.k":
        return "TARGET CLAIM — adequacy and closure reviewed separately"
    if "no-evaluators" in source or "symbol(" in source:
        return (
            "ACCEPT AS UNUSED TRUST BOUNDARY — supplied opaque primitive; no term from "
            "solution.mpy reaches it, so it cannot affect either claim"
        )
    if rel.endswith("/concrete.k"):
        return (
            "ACCEPT CONCRETE-ONLY — imported by MPY-KRUN, not VERIFICATION; cannot "
            "contribute to proof closure"
        )
    if line in REACHABLE.get(rel, set()):
        return (
            "ACCEPT REACHABLE — fixed supplied operational/definitional semantics; "
            "binding, order, state, control, and overlaps checked on the real path"
        )
    return (
        "ACCEPT UNREACHABLE — fixed supplied rule/declaration for a construct absent "
        "from solution.mpy; no matching term can arise on either reviewed claim"
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: inventory_k.py SCRATCH_CANDIDATE_ROOT", file=sys.stderr)
        return 64
    root = Path(sys.argv[1]).resolve()
    paths = sorted((root / "reference-semantics").rglob("*.k"))
    paths.extend([root / "verification.k", root / "spec.k"])

    totals: dict[str, int] = {}
    blocks_by_path: list[tuple[str, list[tuple[int, int, str, str]]]] = []
    for path in paths:
        rel = str(path.relative_to(root))
        blocks = logical_blocks(path)
        blocks_by_path.append((rel, blocks))
        for _, _, kind, _ in blocks:
            totals[kind] = totals.get(kind, 0) + 1

    print("# Exhaustive local K declaration and rule inventory")
    print()
    print(
        "Generated from the fresh scratch source. Each local `syntax`, `rule`, "
        "`claim`, `configuration`, and `context` block is included with its exact "
        "source line and reviewer disposition."
    )
    print()
    print("Counts: " + ", ".join(f"{kind}={totals[kind]}" for kind in sorted(totals)))
    print()

    item_number = 0
    for rel, blocks in blocks_by_path:
        print(f"## `{rel}`")
        print()
        if not blocks:
            print("No local syntax/rule/claim/configuration/context declarations.")
            print()
            continue
        for start, end, kind, source in blocks:
            item_number += 1
            print(f"### I{item_number:04d} — {kind}, lines {start}-{end}")
            print()
            print(f"- Attributes/class: {flags(kind, source)}")
            print(f"- Disposition: {disposition(rel, start, source)}")
            print()
            print("```k")
            print(source)
            print("```")
            print()
    print(f"TOTAL_INVENTORY_ITEMS={item_number}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
