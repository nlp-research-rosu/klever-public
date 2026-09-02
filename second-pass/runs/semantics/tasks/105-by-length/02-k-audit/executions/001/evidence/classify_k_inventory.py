#!/usr/bin/env python3
"""Assign an explicit audit disposition to every inventoried K declaration."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/105-by-length/candidate")
OUTPUT = Path("/audit-output/evidence/k-declaration-dispositions.tsv")
DECLARATION = re.compile(
    r"^(?:"
    r"(requires)\b"
    r"|(module)\b"
    r"|(endmodule)\b"
    r"|  (imports|configuration|syntax|context|rule|claim)\b"
    r")"
)
UNREACHED_HELPERS = {
    "assert.k",
    "comprehension.k",
    "dict.k",
    "float.k",
    "range.k",
    "set.k",
}


def blocks(lines: list[str]):
    starts = [index for index, line in enumerate(lines) if DECLARATION.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        match = DECLARATION.match(lines[start])
        assert match
        kind = next(group for group in match.groups() if group is not None)
        block = "".join(lines[start:end]).rstrip()
        yield kind, start + 1, end, block


def disposition(relative: str, kind: str, line: int, block: str):
    if relative == "verification.k":
        if kind == "rule" and line in {98, 126}:
            return (
                "REJECT_UNSOUND_OPERATIONAL_BRIDGE",
                "No bridge-free connection theorem; arbitrary continuation and "
                "scope footprint are false on the recorded value-binding witness.",
            )
        if line in {9, 10, 49, 50}:
            return (
                "DEFINITION_TRUTHFUL_BUT_UNPINNED",
                "Current proof-local body/closure copy is not linked to solution.mpy.",
            )
        return (
            "ACCEPT_PROOF_LOCAL_DEFINITION",
            "Equation/observer is truthful on its used constructor domain; coverage "
            "limitations and dependents are recorded in REVIEW.md.",
        )
    if relative == "spec.k":
        if kind == "claim":
            return (
                "RESULT_CONSTRAINING_BUT_REJECT_UNPINNED",
                "Destination constrains the result, but source invokes proof-local closure.",
            )
        return ("SPEC_ASSEMBLY", "Module/import declaration.")

    name = Path(relative).name
    if "no-evaluators" in block or "symbol(" in block:
        if name == "sort.k" and "sortVS(ValSeq)" in block:
            return (
                "TRUSTED_FIXED_OPAQUE_BOUNDARY_USED",
                "Supplied sorted() abstraction; concrete LLVM equations and finite "
                "evidence do not constitute a theorem.",
            )
        return (
            "INSPECTED_FIXED_OPAQUE_UNREACHED",
            "Opaque supplied declaration does not occur on the submitted program path.",
        )
    if name in UNREACHED_HELPERS:
        return (
            "INSPECTED_FIXED_UNREACHED",
            "No submitted construct or proof state reaches this declaration.",
        )
    if name == "concrete.k":
        return (
            "INSPECTED_FIXED_CONCRETE_ONLY",
            "Imported only by MPY-KRUN; absent from the target proof definition.",
        )
    if name == "subscript.k" and (
        "valSeqAt(ValSeq, Int)" in block
        or "rule valSeqAt" in block
    ):
        return (
            "CONDITIONAL_FIXED_IN_BOUNDS_BOUNDARY",
            "Equations are sound in bounds; total OOB/opaque cases are underspecified.",
        )
    return (
        "INSPECTED_FIXED_NO_USED_PATH_FALSE_WITNESS",
        "Supplied declaration is routine/relevant or inert; no intended-path false "
        "conclusion was found. Module-level details are in REVIEW.md.",
    )


def main() -> None:
    sources = sorted((ROOT / "reference-semantics").rglob("*.k"))
    sources += [ROOT / "verification.k", ROOT / "spec.k"]
    rows = []
    for path in sources:
        relative = str(path.relative_to(ROOT))
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        for kind, start, end, block in blocks(lines):
            status, reason = disposition(relative, kind, start, block)
            first_line = block.splitlines()[0].strip()
            rows.append(
                (relative, kind, start, end, status, reason, first_line)
            )

    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(
            ["file", "kind", "start_line", "end_line", "disposition", "reason", "source"]
        )
        writer.writerows(rows)
    print(f"declaration_count={len(rows)}")
    print(f"output={OUTPUT}")
    print(f"output_bytes={OUTPUT.stat().st_size}")


if __name__ == "__main__":
    main()
