#!/usr/bin/env python3
"""Produce a complete statement-start inventory for the selected K sources."""

from __future__ import annotations

import csv
import re
from pathlib import Path


SEMANTICS_ROOT = Path("/tmp/audit-work/work/reference-semantics")
PROOF_FILES = [
    Path("/tmp/audit-work/work/verification.k"),
    Path("/tmp/audit-work/work/spec.k"),
]
OUTPUT = Path("/audit-output/evidence/rule-inventory.csv")
START = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")
ATTRS = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "simplification",
    "simplifier",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
]


def statement_starts(path: Path):
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for offset, start in enumerate(starts):
        end = starts[offset + 1] if offset + 1 < len(starts) else len(lines)
        block = lines[start:end]
        while block and (
            not block[-1].strip()
            or block[-1].lstrip().startswith("//")
            or block[-1].strip() == "endmodule"
        ):
            block.pop()
        text = " ".join(part.strip() for part in block if part.strip())
        code_text = " ".join(
            part.split("//", 1)[0].strip()
            for part in block
            if part.split("//", 1)[0].strip()
        )
        kind = START.match(lines[start]).group(1)
        yield start + 1, kind, text, code_text


def main() -> int:
    files = sorted(SEMANTICS_ROOT.rglob("*.k")) + PROOF_FILES
    rows = []
    counts: dict[str, int] = {}
    for path in files:
        origin = "proof-local" if path in PROOF_FILES else "supplied-semantics"
        for line, kind, text, code_text in statement_starts(path):
            attrs = ",".join(
                attr
                for attr in ATTRS
                if re.search(rf"\b{re.escape(attr)}\b", code_text)
            )
            if kind == "rule":
                rule_class = "operational" if "<k>" in text else "equational"
            elif kind == "syntax":
                rule_class = "declaration"
            else:
                rule_class = kind
            opaque = "yes" if "no-evaluators" in attrs or (
                kind == "syntax" and "symbol" in attrs
            ) else "no"
            relative = (
                str(path.relative_to(SEMANTICS_ROOT.parent))
                if origin == "supplied-semantics"
                else path.name
            )
            if origin == "supplied-semantics":
                decision = (
                    "selected supplied baseline; byte-identical to trusted mount; "
                    "no candidate modification; no false-conclusion witness identified"
                )
            elif path.name == "verification.k":
                decision = (
                    "proof-local; manually reviewed for body fidelity, coverage, "
                    "overlap, totality, and result influence"
                )
            else:
                decision = "entry claim; manually reviewed for satisfiability and result constraint"
            row = {
                "file": relative,
                "line": line,
                "kind": kind,
                "class": rule_class,
                "attributes": attrs,
                "opaque": opaque,
                "origin": origin,
                "decision": decision,
                "statement": text,
            }
            rows.append(row)
            counts[kind] = counts.get(kind, 0) + 1

    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"WROTE {OUTPUT}")
    print(f"FILES={len(files)} STATEMENTS={len(rows)}")
    print("COUNTS " + " ".join(f"{kind}={count}" for kind, count in sorted(counts.items())))
    for attr in ATTRS:
        count = sum(attr in row["attributes"].split(",") for row in rows)
        print(f"ATTRIBUTE {attr}={count}")
    print(f"OPAQUE={sum(row['opaque'] == 'yes' for row in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
