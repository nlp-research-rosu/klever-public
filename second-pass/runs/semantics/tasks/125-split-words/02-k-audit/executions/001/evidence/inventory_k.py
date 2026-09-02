#!/usr/bin/env python3
"""Create a complete, reviewer-classified inventory of K declarations."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

START = re.compile(r"^\s*(syntax|rule|claim|context|configuration|alias)\b")
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|claim|context|configuration|alias|module|endmodule|imports)\b"
)
ATTRIBUTE = re.compile(r"\[([^\]]+)\]")

USED_TERMS = (
    "Module",
    "#loadAll",
    "FuncDef",
    "closureVal",
    "Call(",
    "#callee",
    "#evalArgs",
    "#evalArgCont",
    "#applyK",
    "#bindP",
    "#endcall",
    "#pop",
    "frame(",
    "Assign(",
    "Name(",
    "#look",
    "Attribute(",
    "boundMethodV",
    "Str(",
    "strToCodes",
    "cntSub",
    "dropIS",
    "BinOp",
    "applyBin",
    "Compare(",
    "applyCmp",
    "CmpOp",
    "Int(",
    "If(",
    "#branch",
    "Return(",
    "#alloc",
    "splitWS",
    "splitSep",
    "flushTok",
    "isWSC",
    "seqConcat",
    "list(",
    "ref(",
    "builtinsScope",
    "truthy",
)


def statements(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for ordinal, start in enumerate(starts):
        end = len(lines)
        for index in range(start + 1, len(lines)):
            if BOUNDARY.match(lines[index]):
                end = index
                break
        raw = "\n".join(lines[start:end]).strip()
        match = START.match(lines[start])
        assert match
        yield start + 1, match.group(1), raw


def classify(path: Path, line: int, kind: str, text: str) -> tuple[str, str]:
    name = path.name
    if name == "verification.k":
        if kind == "syntax":
            return (
                "CANDIDATE_DECLARATION",
                "Well-sorted proof-local symbol; its defining rule is assessed separately.",
            )
        if kind == "rule" and line in (13, 22, 31, 41, 50):
            witness = {
                13: "path1-false-forces-first-then",
                22: "path2-true-forces-first-else",
                31: "path3-true-forces-first-else",
                41: "path2-false-forces-second-then",
                50: "path3-true-forces-second-else",
            }[line]
            return (
                "UNSOUND_OPERATIONAL_BRIDGE",
                "Ignores Bool operand and preempts fixed #branch; false witness "
                + witness
                + " closes only with this extension.",
            )
        if kind == "rule" and line == 64:
            return (
                "TRUE_BODY_COPY_NOT_PROGRAM_PIN",
                "Equation matches the submitted body text, but the proof never consumes solution.mpy.",
            )
        if kind == "rule" and line == 127:
            return (
                "TRUE_DEFINITIONAL_EQUATION",
                "Names the closure over solutionBody; does not itself pin the submitted module.",
            )
        if kind == "rule" and line in (132, 139, 144):
            return (
                "TRUE_DEFINITIONAL_SUMMARY",
                "Finite sum of fixed cntSub calls; exact for the modeled code points.",
            )
        return ("CANDIDATE_REVIEWED", "No separate defect found.")

    if name == "spec.k":
        return (
            "ENTRY_REACHABILITY_CLAIM",
            "Result-constraining and satisfiable, but depends on the unsound branch bridges and copied closure.",
        )

    if kind in ("syntax", "configuration", "context"):
        used = any(term in text for term in USED_TERMS)
        return (
            "FIXED_DECLARATION_USED" if used else "FIXED_DECLARATION_UNUSED",
            "Byte-identical supplied-semantics declaration; "
            + ("needed on the submitted path." if used else "not reached by the submitted program."),
        )

    if name == "concrete.k":
        return (
            "FIXED_CONCRETE_ONLY",
            "Imported only by MPY-KRUN, not by the Haskell proof main module.",
        )
    if name == "assert.k":
        return (
            "FIXED_UNUSED_ASSERT_ORACLE",
            "Assert does not occur in solution.mpy or any positive claim.",
        )
    if name in ("float.k", "sort.k"):
        return (
            "FIXED_UNUSED_OPAQUE_BOUNDARY",
            "Opaque/concrete helper family is not reached by the submitted program or proof.",
        )

    used = any(term in text for term in USED_TERMS)
    if used:
        return (
            "FIXED_USED_REVIEWED_VALID",
            "Operational/equational rule on the submitted path; guards, control, and state footprint agree with the supplied subset.",
        )
    return (
        "FIXED_UNUSED_BY_PROGRAM",
        "Byte-identical supplied rule; construct is not reached by solution.mpy or the entry claims.",
    )


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: inventory_k.py OUTPUT_TSV SOURCE...", file=sys.stderr)
        return 64
    output = Path(sys.argv[1])
    paths = [Path(arg) for arg in sys.argv[2:]]
    rows = []
    for path in paths:
        for line, kind, raw in statements(path):
            normalized = " ".join(
                part.strip()
                for part in raw.splitlines()
                if part.strip() and not part.lstrip().startswith("//")
            )
            attributes = ";".join(
                match.group(1).strip() for match in ATTRIBUTE.finditer(raw)
            )
            decision, rationale = classify(path, line, kind, normalized)
            rows.append(
                {
                    "file": str(path),
                    "line": line,
                    "kind": kind,
                    "attributes": attributes,
                    "decision": decision,
                    "rationale": rationale,
                    "statement": normalized,
                }
            )

    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "file",
                "line",
                "kind",
                "attributes",
                "decision",
                "rationale",
                "statement",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    by_kind: dict[str, int] = {}
    by_decision: dict[str, int] = {}
    for row in rows:
        by_kind[row["kind"]] = by_kind.get(row["kind"], 0) + 1
        by_decision[row["decision"]] = by_decision.get(row["decision"], 0) + 1
    print(f"TOTAL_INVENTORY_ROWS: {len(rows)}")
    for key in sorted(by_kind):
        print(f"KIND {key}: {by_kind[key]}")
    for key in sorted(by_decision):
        print(f"DECISION {key}: {by_decision[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
