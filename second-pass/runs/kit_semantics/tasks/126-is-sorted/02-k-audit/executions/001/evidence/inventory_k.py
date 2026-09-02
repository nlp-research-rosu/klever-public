#!/usr/bin/env python3
"""Create an exhaustive inventory of supplied and proof-local K statements."""

from __future__ import annotations

import csv
import re
from pathlib import Path


SEMANTICS_ROOT = Path("/tmp/audit-work/126-is-sorted/reference-semantics")
PROOF_ROOT = Path("/tmp/audit-work/126-is-sorted")
OUTPUT_TSV = Path("/audit-output/evidence/stage5-rule-inventory.tsv")
OUTPUT_MD = Path("/audit-output/evidence/stage5-rule-inventory.md")

START = re.compile(
    r"^  (?P<kind>configuration|syntax|rule|claim|context(?: alias)?|alias)\b"
)

# Start lines of the source-relevant semantic slice. Declarations are included
# where they type or configure terms on the actual proof/execution path.
USED_LINES: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60, 61},
    "semantics/core.k": {
        13, 14, 18, 25, 36, 37, 38, 40, 41, 42, 49,
        68, 69, 70, 117, 118, 124, 125, 126, 127, 130,
        131, 132, 152, 157, 158, 185, 186, 189, 190, 191,
        194, 195, 199, 200, 208, 209, 210, 213, 214, 215,
        217, 218, 219,
    },
    "semantics/call.k": {19, 20, 21, 69},
    "semantics/functions.k": {8, 14, 63, 64, 78, 85},
    "semantics/controls.k": {
        9, 20, 51, 52, 53, 54, 65, 69, 71, 72, 73, 85, 106,
    },
    "semantics/operators.k": {10, 15, 16, 17, 38},
    "semantics/int.k": {7, 9, 24},
    "semantics/list.k": {9, 10, 27},
    "semantics/tuple.k": {14, 15, 16, 18, 31, 32},
    "semantics/sort.k": {18, 20, 21, 22, 23, 24, 36},
}


def statements(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group("kind")))
    result: list[tuple[int, str, str]] = []
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[index:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or block_lines[-1].strip() == "endmodule"
        ):
            block_lines.pop()
        result.append((index + 1, kind, "\n".join(block_lines)))
    return result


def subtype(kind: str, block: str) -> str:
    attributes = " ".join(re.findall(r"\[[^\]]+\]", block))
    if kind == "syntax":
        tags = ["syntax"]
        for name in (
            "function",
            "total",
            "functional",
            "macro",
            "symbol",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(name)}\b", attributes):
                tags.append(name)
        return "+".join(tags)
    if kind == "rule":
        if "simplification" in attributes:
            return "simplification-rule"
        if "priority(" in attributes or "[priority]" in attributes:
            return "priority-rule"
        if "concrete" in attributes:
            return "concrete-rule"
        if "owise" in attributes:
            return "owise-rule"
        return "ordinary-rule"
    return kind.replace(" ", "-")


def main() -> int:
    paths = sorted(SEMANTICS_ROOT.rglob("*.k"))
    paths.extend([PROOF_ROOT / "verification.k", PROOF_ROOT / "spec.k"])
    rows: list[dict[str, str | int]] = []
    counts: dict[str, int] = {}

    for path in paths:
        if path.is_relative_to(SEMANTICS_ROOT):
            rel = path.relative_to(SEMANTICS_ROOT).as_posix()
            origin = "supplied-fixed-semantics"
            proof_use = "source-relevant" if (
                rel in USED_LINES
            ) else "not-on-source-path"
            decision = (
                "selected fixed-semantics statement; audited in used slice"
                if proof_use == "source-relevant"
                else "selected fixed-semantics statement; no dependency from "
                     "submitted program or proof path"
            )
        else:
            rel = path.name
            origin = (
                "candidate-proof-extension"
                if path.name == "verification.k"
                else "candidate-reachability-claim"
            )
            proof_use = "source-relevant"
            decision = "manual rule-by-rule decision in REVIEW.md"

        for line, kind, block in statements(path):
            if origin == "supplied-fixed-semantics":
                proof_use = (
                    "source-relevant"
                    if line in USED_LINES.get(rel, set())
                    else "not-on-source-path"
                )
                decision = (
                    "selected fixed-semantics statement; audited in used slice"
                    if proof_use == "source-relevant"
                    else "selected fixed-semantics statement; no dependency "
                         "from submitted program or proof path"
                )
            record_type = subtype(kind, block)
            counts[record_type] = counts.get(record_type, 0) + 1
            rows.append(
                {
                    "id": f"K{len(rows) + 1:04d}",
                    "file": rel,
                    "line": line,
                    "origin": origin,
                    "record_type": record_type,
                    "proof_use": proof_use,
                    "decision": decision,
                    "statement": " ".join(block.split()),
                }
            )

    with OUTPUT_TSV.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "id",
                "file",
                "line",
                "origin",
                "record_type",
                "proof_use",
                "decision",
                "statement",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    with OUTPUT_MD.open("w") as stream:
        stream.write("# Exhaustive K statement inventory\n\n")
        stream.write(
            "Each row is one top-level configuration, syntax declaration, "
            "context, rule, or claim from the supplied semantics and the "
            "candidate proof sources. Multiline statements are flattened "
            "without changing tokens.\n\n"
        )
        stream.write(
            "| ID | File:line | Origin | Type | Path use | Decision |\n"
            "|---|---|---|---|---|---|\n"
        )
        for row in rows:
            stream.write(
                f"| {row['id']} | `{row['file']}:{row['line']}` | "
                f"{row['origin']} | {row['record_type']} | "
                f"{row['proof_use']} | {row['decision']} |\n"
            )
        stream.write("\n## Full statements\n\n")
        for row in rows:
            stream.write(
                f"### {row['id']} — `{row['file']}:{row['line']}`\n\n"
                f"- Origin: {row['origin']}\n"
                f"- Type: {row['record_type']}\n"
                f"- Path use: {row['proof_use']}\n"
                f"- Decision: {row['decision']}\n\n"
                f"```k\n{row['statement']}\n```\n\n"
            )

    print(f"source_files={len(paths)}")
    print(f"inventory_records={len(rows)}")
    for kind, count in sorted(counts.items()):
        print(f"{kind}={count}")
    print(
        "source_relevant_records="
        f"{sum(row['proof_use'] == 'source-relevant' for row in rows)}"
    )
    print(f"tsv={OUTPUT_TSV}")
    print(f"markdown={OUTPUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
