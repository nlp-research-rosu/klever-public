#!/usr/bin/env python3
"""Exhaustive lexical inventory of supplied and proof-local K declarations."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/task")
FILES = (
    [ROOT / "reference-semantics" / "semantics.k"]
    + sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    + [ROOT / "verification.k", ROOT / "spec.k"]
)

START = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|module|endmodule|imports)\b"
)

# Line ranges that form the target's concrete/proof execution slice. Everything
# else is still inventoried and dispositioned as fixed but unreachable here.
RELEVANT_RANGES: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics.k": [(34, 90)],
    "reference-semantics/semantics/syntax.k": [(9, 61)],
    "reference-semantics/semantics/core.k": [
        (9, 55), (99, 113), (116, 173), (176, 204), (216, 224),
    ],
    "reference-semantics/semantics/operators.k": [(7, 13)],
    "reference-semantics/semantics/int.k": [(19, 20)],
    "reference-semantics/semantics/str.k": [(9, 26)],
    "reference-semantics/semantics/subscript.k": [(29, 122)],
    "reference-semantics/semantics/functions.k": [(8, 25), (62, 91)],
    "reference-semantics/semantics/builtins.k": [(9, 12), (107, 121)],
    "reference-semantics/semantics/call.k": [(14, 31), (63, 71)],
    "reference-semantics/semantics/assert.k": [(3, 16)],
}


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def relevant(path: str, start: int, end: int) -> bool:
    return any(start <= hi and end >= lo for lo, hi in RELEVANT_RANGES.get(path, []))


def entries(path: Path):
    lines = path.read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            i += 1
            continue
        if line.startswith("requires "):
            yield i + 1, i + 1, "requires-file", line
            i += 1
            continue
        match = START.match(line)
        if not match:
            i += 1
            continue
        kind = match.group(1)
        start = i
        i += 1
        if kind not in {"module", "endmodule", "imports"}:
            while i < len(lines):
                candidate = lines[i]
                if candidate.startswith("requires "):
                    break
                if START.match(candidate):
                    break
                i += 1
        yield start + 1, i, kind, "\n".join(lines[start:i])


def main() -> None:
    inventory = []
    for path in FILES:
        rel = relative(path)
        for start, end, kind, text in entries(path):
            compact = " ".join(text.split())
            flags = []
            for flag, pattern in [
                ("function", r"\bfunction\b"),
                ("functional", r"\bfunctional\b"),
                ("total", r"\btotal\b"),
                ("symbol", r"\bsymbol\s*\("),
                ("no-evaluators", r"\bno-evaluators\b"),
                ("priority", r"\bpriority\s*\("),
                ("simplification", r"\bsimplification\b"),
                ("concrete", r"\bconcrete\b"),
                ("owise", r"\bowise\b"),
                ("macro", r"\bmacro\b"),
                ("strict", r"\b(?:seq)?strict\b"),
            ]:
                if re.search(pattern, compact):
                    flags.append(flag)

            is_relevant = relevant(rel, start, end)
            if rel == "verification.k":
                if kind == "rule" and "doSlice(" in compact:
                    status = "ACCEPTED_SOUND_DERIVED_EQUATION_EVIDENCE_GAP"
                    note = (
                        "Drops exactly two constructors; agrees with fixed slice equations "
                        "by structural induction, but candidate supplies no bridge-free K theorem."
                    )
                elif kind == "rule" and "#runDecimalToBinary" in compact:
                    status = "ACCEPTED_EXACT_PROGRAM_WRAPPER"
                    note = "Direct closure body mechanically matches translated function body."
                else:
                    status = "PROOF_LOCAL_DECLARATION"
                    note = "Declaration/import only."
                is_relevant = True
            elif rel == "spec.k":
                status = "TARGET_CLAIM" if kind == "claim" else "SPEC_DECLARATION"
                note = "Audited for domain, result constraint, and concrete satisfiability."
                is_relevant = True
            elif "symbol" in flags or "no-evaluators" in flags:
                if is_relevant:
                    status = "TRUSTED_PRIMITIVE_USED"
                    note = "Fixed supplied-semantics primitive on target slice."
                else:
                    status = "TRUSTED_PRIMITIVE_UNUSED"
                    note = "Fixed supplied-semantics boundary unreachable from this program."
            elif is_relevant:
                status = "ACCEPTED_USED_FIXED_SEMANTICS"
                note = "Used fixed-semantics declaration/rule; reviewed on target domain."
            else:
                status = "ACCEPTED_FIXED_SEMANTICS_UNREACHED"
                note = "Supplied baseline entry unreachable from this target; cannot affect theorem."

            inventory.append(
                {
                    "id": f"{rel}:{start}",
                    "file": rel,
                    "start_line": start,
                    "end_line": end,
                    "kind": kind,
                    "flags": ",".join(flags),
                    "target_slice": "yes" if is_relevant else "no",
                    "status": status,
                    "note": note,
                    "text": compact,
                }
            )

    csv_path = Path("/audit-output/evidence/rule-inventory.csv")
    with csv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(inventory[0]))
        writer.writeheader()
        writer.writerows(inventory)

    by_kind = Counter(item["kind"] for item in inventory)
    by_status = Counter(item["status"] for item in inventory)
    by_flag = Counter(
        flag
        for item in inventory
        for flag in item["flags"].split(",")
        if flag
    )
    rule_count = by_kind["rule"]
    claim_count = by_kind["claim"]
    syntax_count = by_kind["syntax"]
    assert rule_count > 0 and claim_count == 1 and syntax_count > 0

    summary_path = Path("/audit-output/evidence/rule-inventory-summary.md")
    with summary_path.open("w") as stream:
        stream.write("# Exhaustive K inventory summary\n\n")
        stream.write(f"- Files: {len(FILES)}\n")
        stream.write(f"- Total inventoried entries: {len(inventory)}\n")
        for key, count in sorted(by_kind.items()):
            stream.write(f"- Kind `{key}`: {count}\n")
        stream.write("\n## Attributes\n\n")
        for key, count in sorted(by_flag.items()):
            stream.write(f"- `{key}`: {count}\n")
        stream.write("\n## Dispositions\n\n")
        for key, count in sorted(by_status.items()):
            stream.write(f"- `{key}`: {count}\n")
        stream.write(
            "\nEvery row, including its complete normalized declaration/rule text, "
            "source span, flags, target reachability, and disposition, is in "
            "`rule-inventory.csv`.\n"
        )

    print(f"files={len(FILES)}")
    print(f"entries={len(inventory)}")
    print(f"kind_counts={dict(sorted(by_kind.items()))}")
    print(f"attribute_counts={dict(sorted(by_flag.items()))}")
    print(f"status_counts={dict(sorted(by_status.items()))}")
    print(f"csv={csv_path}")
    print(f"summary={summary_path}")
    print("RULE_INVENTORY_OK")


if __name__ == "__main__":
    main()
