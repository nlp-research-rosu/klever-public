#!/usr/bin/env python3
"""Create a source-location-complete K declaration/rule inventory."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path("/tmp/audit-work/21-rescale-to-unit")
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.txt")
START = re.compile(r"^\s*(configuration|syntax|rule|claim|context)\b")
STOP = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context|module|endmodule|imports)\b"
)


def classify(path: Path, line: int, kind: str) -> str:
    relative = str(path.relative_to(ROOT))
    if relative.startswith("reference-semantics/"):
        return "SUPPLIED_BASELINE_FIXED"
    if relative == "spec.k":
        return "ILLEGIT_CIRCULAR_POSTCONDITION" if kind == "claim" else "SPEC_DECLARATION"
    if relative != "verification.k":
        return "REVIEWER_OR_OTHER"
    if line in (9,):
        return "ILLEGIT_RESULT_ORACLE_DECLARATION"
    if line in (12, 15):
        return "UNSOUND_OPERATIONAL_RESULT_BRIDGE"
    if line == 21:
        return "NARROW_EQUATION_SOUND_TOTALITY_OVERBROAD"
    if line == 22:
        return "SOUND_FLOAT_PROJECTION_EQUATION"
    if line in (24, 25):
        return "SOUND_DEFINITIONAL_FLOAT_SUMMARY"
    if line in (28, 29, 30):
        return "SOUND_TERMINATING_LIST_SUMMARY"
    if line in (37, 38, 39):
        return "SOUND_TERMINATING_DOMAIN_PREDICATE"
    if line in (44, 45, 46, 47):
        return "SOUND_UNUSED_TYPED_GENERATOR"
    if line == 54:
        return "UNSOUND_OPERATIONAL_COMPREHENSION_BRIDGE"
    if line in (85, 86):
        return "SOUND_OBSERVATION_HARNESS"
    if line in (91, 92):
        return "SOUND_SYNTACTIC_RUN_HARNESS_WITH_INPUT_BRIDGE_LIMITATION"
    return "REQUIRES_MANUAL_REVIEW"


def flags(block: str, kind: str) -> str:
    found = []
    for name in (
        "function",
        "total",
        "functional",
        "no-evaluators",
        "symbol",
        "priority",
        "simplification",
        "concrete",
        "owise",
        "macro",
        "strict",
        "seqstrict",
        "token",
        "bracket",
        "assoc",
        "comm",
        "idem",
        "unit",
    ):
        if re.search(rf"\b{re.escape(name)}\b", block):
            found.append(name)
    if kind == "rule" and not any(
        name in found for name in ("simplification", "concrete", "macro")
    ):
        found.append("ordinary")
    return ",".join(found) if found else "-"


def declarations(path: Path) -> list[dict[str, str | int]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [(index, START.match(text)) for index, text in enumerate(lines)]
    records = []
    for index, match in starts:
        if match is None:
            continue
        end = index + 1
        while end < len(lines) and not STOP.match(lines[end]):
            end += 1
        block_lines = lines[index:end]
        while len(block_lines) > 1 and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        block = "\n".join(block_lines).strip()
        kind = match.group(1)
        records.append(
            {
                "file": str(path.relative_to(ROOT)),
                "line": index + 1,
                "kind": kind,
                "flags": flags(block, kind),
                "review_decision": classify(path, index + 1, kind),
                "source": " ".join(block.split()),
            }
        )
    return records


def main() -> None:
    paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])
    records = [record for path in paths for record in declarations(path)]
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=("file", "line", "kind", "flags", "review_decision", "source"),
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(records)

    by_kind = Counter(str(record["kind"]) for record in records)
    by_decision = Counter(str(record["review_decision"]) for record in records)
    by_file = Counter(str(record["file"]) for record in records)
    by_flag: Counter[str] = Counter()
    for record in records:
        for flag in str(record["flags"]).split(","):
            if flag != "-":
                by_flag[flag] += 1
    lines = [
        f"files={len(paths)}",
        f"records={len(records)}",
        "kind_counts=" + ",".join(f"{key}:{by_kind[key]}" for key in sorted(by_kind)),
        "flag_counts=" + ",".join(f"{key}:{by_flag[key]}" for key in sorted(by_flag)),
        "decision_counts="
        + ",".join(f"{key}:{by_decision[key]}" for key in sorted(by_decision)),
        "per_file:",
    ]
    lines.extend(f"{name}\t{by_file[name]}" for name in sorted(by_file))
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(SUMMARY.read_text(encoding="utf-8"), end="")
    print(f"inventory={OUTPUT}")


if __name__ == "__main__":
    main()
