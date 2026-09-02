#!/usr/bin/env python3
"""Create an exhaustive textual inventory of supplied and proof-local K items."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


REFERENCE_ROOT = Path("/reference/reference-semantics")
VERIFICATION = Path("/candidate/verification.k")
SPEC = Path("/candidate/spec.k")
OUTPUT = Path("/audit-output/evidence/11-static-inventory.tsv")

START = re.compile(
    r"^\s*(configuration|syntax|context(?:\s+alias)?|rule|claim|alias)\b"
)


def statements(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1).replace(" ", "_")))
    for position, (start, kind) in enumerate(starts):
        limit = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = limit
        while end > start + 1:
            stripped = lines[end - 1].strip()
            if stripped == "" or stripped.startswith("//") or stripped == "endmodule":
                end -= 1
            else:
                break
        text = " ".join(part.strip() for part in lines[start:end] if part.strip())
        yield start + 1, end, kind, text


def attributes(text: str) -> str:
    names = [
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "priority",
        "owise",
        "concrete",
        "simplification",
        "simplifier",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
        "anywhere",
    ]
    return ",".join(name for name in names if name in text)


def local_disposition(line: int, kind: str) -> tuple[str, str]:
    if kind == "syntax":
        if line in {9, 11, 13, 14}:
            return (
                "UNJUSTIFIED_OPAQUE_RESULT",
                "result-bearing observation lacks equations/connection theorem",
            )
        return ("DECLARATION", "proof-local constructor/helper declaration")
    if kind != "rule":
        return ("DECLARATION", "non-rule proof-local item")
    if line == 19:
        return ("UNSOUND_BRIDGE", "W1 count result can differ from fixed cntSub")
    if line == 27:
        return ("UNSOUND_BRIDGE", "W2 head result can differ from fixed intSeqAt")
    if line == 34:
        return ("UNSOUND_BRIDGE", "W3 suffix result can differ from fixed doSlice/buildIS")
    if line == 42:
        return ("UNSOUND_BRIDGE", "W4 .txt equality can differ from fixed string equality")
    if line == 48:
        return ("UNSOUND_BRIDGE", "W5 .exe equality can differ from fixed string equality")
    if line == 54:
        return ("UNSOUND_BRIDGE", "W6 .dll equality can differ from fixed string equality")
    if line in {62, 67, 71}:
        return ("VALID_DEFINITION", "truthful composition, conditional on observation meanings")
    if line == 81:
        return ("VALID_PINNING_DEFINITION", "constructor-identical submitted function body")
    if line == 170:
        return ("VALID_EXACT_HELPER", "exact one-function module projection used at one ground term")
    if line == 175:
        return ("VALID_ENTRY_WRAPPER", "constructs exact closure/body and executes ordinary call rules")
    return ("REVIEW_NEEDED", "unclassified local rule")


def main() -> int:
    rows: list[dict[str, object]] = []
    all_paths = sorted(REFERENCE_ROOT.rglob("*.k")) + [VERIFICATION, SPEC]
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for path in all_paths:
        if path == VERIFICATION:
            origin = "PROOF_LOCAL"
        elif path == SPEC:
            origin = "TARGET_SPEC"
        else:
            origin = "SUPPLIED_SEMANTICS"
        display = str(path)
        for start, end, kind, text in statements(path):
            attrs = attributes(text)
            if origin == "PROOF_LOCAL":
                disposition, rationale = local_disposition(start, kind)
            elif origin == "TARGET_SPEC":
                disposition = "TARGET_CLAIM"
                rationale = "audited for adequacy and non-vacuity separately"
            else:
                disposition = "SELECTED_FIXED_MODEL"
                if "no-evaluators" in attrs:
                    rationale = "explicit supplied-semantics opaque boundary; unused by submitted program"
                elif "concrete" in attrs:
                    rationale = "supplied concrete-only equation; unused in symbolic submitted path"
                else:
                    rationale = "task-generic rule/declaration in byte-verified supplied baseline"
            rows.append(
                {
                    "origin": origin,
                    "file": display,
                    "start_line": start,
                    "end_line": end,
                    "kind": kind,
                    "attributes": attrs,
                    "disposition": disposition,
                    "rationale": rationale,
                    "statement": text,
                }
            )
            counts[display][kind] += 1

    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "origin",
                "file",
                "start_line",
                "end_line",
                "kind",
                "attributes",
                "disposition",
                "rationale",
                "statement",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"output={OUTPUT}")
    print(f"inventory_rows={len(rows)}")
    for path in all_paths:
        display = str(path)
        count_text = ",".join(
            f"{kind}={count}" for kind, count in sorted(counts[display].items())
        )
        print(f"{display}: {count_text}")
    dispositions = Counter(str(row["disposition"]) for row in rows)
    print(f"dispositions={dict(sorted(dispositions.items()))}")
    opaque = [
        row
        for row in rows
        if "no-evaluators" in str(row["attributes"])
        or row["disposition"] == "UNJUSTIFIED_OPAQUE_RESULT"
    ]
    print(f"opaque_or_no_evaluator_rows={len(opaque)}")
    for row in opaque:
        print(
            f"  {row['file']}:{row['start_line']} "
            f"{row['disposition']} {row['statement']}"
        )
    unclassified = [row for row in rows if row["disposition"] == "REVIEW_NEEDED"]
    print(f"unclassified_proof_local_rows={len(unclassified)}")
    return int(bool(unclassified))


if __name__ == "__main__":
    raise SystemExit(main())
