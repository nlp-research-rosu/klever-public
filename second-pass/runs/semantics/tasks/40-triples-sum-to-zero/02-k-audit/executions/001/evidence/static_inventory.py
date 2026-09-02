#!/usr/bin/env python3
"""Create a declaration-by-declaration inventory of all submitted K sources."""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/forty-triples-audit/candidate-src")
OUTPUT = Path("/audit-output/evidence/static-inventory.tsv")
START = re.compile(r"^\s*(configuration|context|syntax|rule|claim)\b")
BOUNDARY = re.compile(r"^\s*(module|endmodule)\b")


def normalized(lines: list[str]) -> str:
    kept = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        kept.append(stripped)
    return " ".join(kept)


def flags(text: str) -> list[str]:
    names = [
        "function",
        "total",
        "functional",
        "symbol",
        "no-evaluators",
        "simplification",
        "concrete",
        "owise",
        "macro-rec",
        "macro",
        "strict",
        "seqstrict",
        "priority",
    ]
    return [name for name in names if re.search(rf"\b{re.escape(name)}\b", text)]


def role(path: Path, start: int, kind: str, text: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "verification.k":
        if kind == "rule" and start <= 24:
            return "proof_definitional_equation"
        if kind == "rule":
            return "proof_synthetic_entry_operational_rule"
        if "#runTriples" in text:
            return "proof_synthetic_entry_syntax"
        return "proof_summary_syntax"
    if rel == "spec.k":
        return "positive_target_claim"
    if kind == "configuration":
        return "fixed_configuration"
    if kind == "context":
        return "fixed_evaluation_context"
    if kind == "syntax" and "no-evaluators" in text:
        return "fixed_opaque_symbol"
    if kind == "syntax":
        return "fixed_syntax_or_function_declaration"
    if kind == "rule" and "[concrete]" in text:
        return "fixed_concrete_rule"
    if kind == "rule" and "<k>" in text:
        return "fixed_operational_rule"
    if kind == "rule":
        return "fixed_equational_rule"
    return "fixed_other"


def decision(rel: str, role_name: str) -> str:
    if rel.startswith("reference-semantics/"):
        return (
            "ACCEPTED_SELECTED_SEMANTICS:"
            "byte-identical-to-trusted-supplied-tree"
        )
    if role_name == "proof_definitional_equation":
        return "VALID:structural-existential-equation-on-Int-ValSeq"
    if role_name == "proof_synthetic_entry_operational_rule":
        return (
            "GAP:defines-manual-closure-execution-but-has-no-connection-claim-"
            "to-loaded-solution.mpy"
        )
    if role_name == "proof_synthetic_entry_syntax":
        return "GAP:synthetic-entry-not-the-submitted-Module-entry"
    if role_name == "proof_summary_syntax":
        return "VALID:defined-by-disjoint-structurally-recursive-equations"
    if role_name == "positive_target_claim":
        return (
            "LIMITED:result-constraining-but-only-exact-length-0-through-6-"
            "and-targets-synthetic-entry"
        )
    return "REVIEWED"


def declarations(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (index, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        for boundary in range(index + 1, stop):
            if BOUNDARY.match(lines[boundary]):
                stop = boundary
                break
        block = lines[index:stop]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        text = normalized(block)
        yield index + 1, index + len(block), kind, text


def main() -> int:
    paths = [ROOT / "reference-semantics/semantics.k"]
    paths.extend(sorted((ROOT / "reference-semantics/semantics").glob("*.k")))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])

    rows = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        for start, end, kind, text in declarations(path):
            role_name = role(path, start, kind, text)
            rows.append(
                {
                    "id": len(rows) + 1,
                    "file": rel,
                    "start_line": start,
                    "end_line": end,
                    "kind": kind,
                    "flags": ",".join(flags(text)) or "none",
                    "role": role_name,
                    "review_decision": decision(rel, role_name),
                    "text": text,
                }
            )

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "id",
                "file",
                "start_line",
                "end_line",
                "kind",
                "flags",
                "role",
                "review_decision",
                "text",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    kind_counts = Counter(row["kind"] for row in rows)
    role_counts = Counter(row["role"] for row in rows)
    flag_counts = Counter(
        flag
        for row in rows
        for flag in row["flags"].split(",")
        if flag != "none"
    )
    print(f"INVENTORY_PATH {OUTPUT}")
    print(f"INVENTORY_SHA256 {hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}")
    print(f"INVENTORY_ROW_COUNT {len(rows)}")
    for key, value in sorted(kind_counts.items()):
        print(f"KIND_COUNT {key} {value}")
    for key, value in sorted(role_counts.items()):
        print(f"ROLE_COUNT {key} {value}")
    for key, value in sorted(flag_counts.items()):
        print(f"FLAG_COUNT {key} {value}")
    print(f"FLAG_COUNT functional {flag_counts['functional']}")
    print(f"FLAG_COUNT simplification {flag_counts['simplification']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
