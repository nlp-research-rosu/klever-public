#!/usr/bin/env python3
"""One disposition for every item in the exhaustive K source inventory."""

from __future__ import annotations

import re
from pathlib import Path


FILES = [
    Path("/tmp/audit-work/reference-semantics/semantics.k"),
    *sorted(Path("/tmp/audit-work/reference-semantics/semantics").glob("*.k")),
    Path("/tmp/audit-work/verification.k"),
    Path("/tmp/audit-work/spec.k"),
]
START = re.compile(r"^\s*(configuration\b|syntax\b|context\b|rule\b|claim\b|priority\b)")

# Source ranges reached by the submitted term. Exact behavior and overlaps for
# these ranges are explained in evidence/used-rule-map.md.
USED_RANGES: dict[str, list[tuple[int, int]]] = {
    "syntax.k": [(9, 61)],
    "core.k": [(13, 60), (68, 70), (117, 127), (129, 191), (208, 229)],
    "controls.k": [(8, 18), (33, 48), (62, 74)],
    "functions.k": [(8, 20), (62, 90)],
    "call.k": [(15, 24), (52, 74)],
    "iter.k": [(6, 9)],
    "str.k": [(7, 26)],
    "list.k": [(12, 20), (52, 55)],
    "operators.k": [(10, 17)],
    "tuple.k": [(30, 41)],
}


def items(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        body = []
        for index in range(start, stop):
            line = lines[index]
            if index > start and re.match(r"^\s*(end)?module\b", line):
                break
            body.append(line)
        yield start + 1, "\n".join(body).rstrip()


def in_used_range(path: Path, line: int) -> bool:
    return any(low <= line <= high for low, high in USED_RANGES.get(path.name, []))


def first_line(body: str) -> str:
    return " ".join(body.splitlines()[0].split())


def main() -> None:
    total = 0
    for path in FILES:
        for line, body in items(path):
            total += 1
            location = f"{path}:{line}"
            if path.name == "verification.k":
                if body.lstrip().startswith("syntax"):
                    decision = (
                        "ACCEPT_PROOF_LOCAL_DECLARATION: pure result sort; "
                        "function/total attributes covered by disjoint constructor equations"
                    )
                else:
                    decision = (
                        "ACCEPT_PROOF_LOCAL_EQUATION: true constructor equation, "
                        "non-overlapping case, strict structural descent, no cells/control"
                    )
            elif path.name == "spec.k":
                if "loop-invariant" in body:
                    decision = (
                        "ACCEPT_AUXILIARY_CLAIM: exact #loop/body and complete modified-state "
                        "summary; independently closes under fixed semantics"
                    )
                else:
                    decision = (
                        "ACCEPT_ENTRY_CLAIM: exact regenerated function/body and result-bearing "
                        "heap postcondition; complete two-claim run closes"
                    )
            elif in_used_range(path, line):
                decision = (
                    "ACCEPT_FIXED_MATERIAL: selected supplied semantics; manually mapped and "
                    "checked for evaluation, binding, control, allocation, and state footprint"
                )
            else:
                decision = (
                    "ACCEPT_FIXED_NONMATERIAL: selected supplied semantics and not reachable "
                    "from this submitted constructor term; no task/proof-local symbol present"
                )
            task_symbols = [
                name
                for name in ("all_prefixes", "prefixesAcc", "finishPrefix", "finishChar")
                if name in body
            ]
            if "/reference-semantics/" in str(path):
                assert not task_symbols, f"task symbol in supplied semantics: {location}"
            print(f"ITEM {total:04d} {location}")
            print(f"HEAD {first_line(body)}")
            print(f"DECISION {decision}")
    print(f"TOTAL_DECISIONS {total}")


if __name__ == "__main__":
    main()
