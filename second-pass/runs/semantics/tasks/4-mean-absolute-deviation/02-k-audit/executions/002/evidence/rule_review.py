#!/usr/bin/env python3
"""Per-rule audit disposition layered over the exhaustive raw inventory."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
FIXED_ROOT = ROOT / "reference-semantics"
FILES = [
    FIXED_ROOT / "semantics.k",
    *sorted((FIXED_ROOT / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

TARGET_PATH_FILES = {
    "semantics.k",
    "semantics/syntax.k",
    "semantics/core.k",
    "semantics/iter.k",
    "semantics/operators.k",
    "semantics/float.k",
    "semantics/list.k",
    "semantics/controls.k",
    "semantics/functions.k",
    "semantics/builtins.k",
    "semantics/call.k",
}


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def blocks(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if re.match(r"^\s*(rule|claim)\b", line)
    ]
    result: list[tuple[int, str, str]] = []
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        # Stop before a new declaration/module boundary.
        for index in range(start + 1, stop):
            if re.match(
                r"^\s*(syntax|context|configuration|module|endmodule|imports|requires)\b",
                lines[index],
            ):
                stop = index
                break
        kind = re.match(r"^\s*(rule|claim)", lines[start]).group(1)  # type: ignore[union-attr]
        result.append((start + 1, kind, one_line("\n".join(lines[start:stop]))))
    return result


def verification_disposition(line: int) -> tuple[str, str]:
    if line == 10:
        return (
            "ACCEPT",
            "truthful definitional name for exact submitted Module constructor term",
        )
    if line == 28:
        return (
            "ACCEPT",
            "entry orchestration loads exact module then performs ordinary named call",
        )
    if 35 <= line <= 40:
        return (
            "ACCEPT",
            "structural, terminating, disjoint/exhaustive predicate equation",
        )
    if 53 <= line <= 62:
        return (
            "ACCEPT",
            "structural, terminating fold equation using supplied float primitives",
        )
    if line == 64:
        return (
            "GAP",
            "operational sum acceleration has no bridge-free candidate connection theorem; "
            "its equations mirror the fixed fold and no false witness was found",
        )
    if line == 70:
        return (
            "REJECT_UNSOUND",
            "operational loop bridge omits for-target binding; machine witness proves a "
            "state excluded by fixed execution",
        )
    return ("REVIEW", "unrecognized proof-local rule")


def main() -> None:
    print("file\tline\tkind\tattributes\tdisposition\treason\thead")
    counts: dict[str, int] = {}
    for path in FILES:
        relative = path.relative_to(ROOT).as_posix()
        for line, kind, head in blocks(path):
            attributes = ",".join(
                attribute
                for attribute in (
                    "priority" if "[priority(" in head else "",
                    "owise" if "[owise]" in head else "",
                    "concrete" if "[concrete]" in head else "",
                    "simplification" if "simplification" in head else "",
                )
                if attribute
            )
            if path == ROOT / "verification.k":
                disposition, reason = verification_disposition(line)
            elif path == ROOT / "spec.k":
                disposition, reason = (
                    "TARGET_CLAIM",
                    "result-constraining reachability claim; dynamic closure audited separately",
                )
            else:
                fixed_relative = path.relative_to(FIXED_ROOT).as_posix()
                if fixed_relative in TARGET_PATH_FILES:
                    disposition, reason = (
                        "SUPPLIED_BASELINE_TARGET_PATH",
                        "byte-identical launcher-selected semantics; used-rule mapping and "
                        "trust primitives reviewed in REVIEW.md; no candidate modification",
                    )
                else:
                    disposition, reason = (
                        "SUPPLIED_BASELINE_UNUSED",
                        "byte-identical launcher-selected semantics and unreachable from this "
                        "program/claim; no proof dependency",
                    )
            counts[disposition] = counts.get(disposition, 0) + 1
            print(
                f"{relative}\t{line}\t{kind}\t{attributes}\t{disposition}\t"
                f"{reason}\t{head[:300]}"
            )
    print("# counts=" + repr(dict(sorted(counts.items()))))


if __name__ == "__main__":
    main()
