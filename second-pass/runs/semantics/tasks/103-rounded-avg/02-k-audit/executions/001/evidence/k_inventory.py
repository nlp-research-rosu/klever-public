#!/usr/bin/env python3
"""Build an exhaustive, line-addressable inventory of local K declarations."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
EVIDENCE = Path("/audit-output/evidence")
START = re.compile(r"^\s*(configuration|syntax|rule|claim|context)\b")
KNOWN_ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "owise",
    "no-evaluators",
    "macro-rec",
    "macro",
    "seqstrict",
    "strict",
    "token",
    "bracket",
)


@dataclass
class Entry:
    source: Path
    start: int
    end: int
    kind: str
    text: str


def logical_entries(path: Path) -> list[Entry]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    entries: list[Entry] = []
    for position, (index, kind) in enumerate(starts):
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        chunk = lines[index:next_index]
        while chunk and (
            not chunk[-1].strip() or chunk[-1].lstrip().startswith("//")
        ):
            chunk.pop()
        entries.append(
            Entry(
                source=path,
                start=index + 1,
                end=index + len(chunk),
                kind=kind,
                text="\n".join(chunk),
            )
        )
    return entries


def tags(text: str) -> list[str]:
    code = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
    attribute_text = "\n".join(re.findall(r"\[([^\[\]]*)\]", code))
    found: list[str] = []
    for attribute in KNOWN_ATTRIBUTES:
        if re.search(rf"\b{re.escape(attribute)}\b", attribute_text):
            found.append(attribute)
    found.extend(re.findall(r"priority\(\d+\)", attribute_text))
    found.extend(re.findall(r"symbol\([^)]*\)", attribute_text))
    found.extend(re.findall(r"hook\([^)]*\)", attribute_text))
    return sorted(set(found))


def role(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative.startswith("reference-semantics/"):
        return "trusted-supplied-semantics"
    if relative == "verification.k":
        return "candidate-proof-extension"
    if relative == "spec.k":
        return "candidate-target-claim"
    return "reviewer"


USED_MARKERS = (
    "Module",
    "#loadAll",
    "Stmts",
    "FuncDef",
    "closureVal",
    "#bindP",
    "#endcall",
    "#pop",
    "frame(",
    "Return(",
    "Name(",
    "#look",
    "Assign(",
    "If(",
    "#branch",
    "truthy",
    "Int(",
    "UnaryOp(",
    "BinOp(",
    "Compare(",
    "CmpOp(",
    "applyUn",
    "applyBin",
    "applyCmp",
    "pyMod",
    "Call(",
    "#callee",
    "#evalArgs",
    "#evalArgCont",
    "#applyK",
    "applyBuiltin",
    "builtinsScope",
    "binCodes",
    "binAcc",
    "roundedAvg",
)


def usage(entry: Entry) -> str:
    if entry.source.name in {"verification.k", "spec.k"}:
        return "direct"
    return "candidate-path" if any(marker in entry.text for marker in USED_MARKERS) else "unused"


def assessment(entry: Entry) -> str:
    entry_role = role(entry.source)
    if entry_role == "trusted-supplied-semantics":
        if "no-evaluators" in tags(entry.text) or "symbol(" in entry.text:
            return "ACCEPTED_FIXED_BASELINE_OPAQUE_BOUNDARY"
        return "ACCEPTED_FIXED_BASELINE"
    if entry_role == "candidate-proof-extension":
        if "roundedAvgCall" in entry.text:
            return "LOCALLY_SOUND_DIRECT_CALL_HARNESS_MANUAL_PIN"
        if "roundedAvgBody" in entry.text:
            return "LOCALLY_SOUND_TRANSPARENT_AST_ALIAS_MANUAL_PIN"
        return "REVIEWED_CANDIDATE_EXTENSION"
    if entry_role == "candidate-target-claim":
        return "RESULT_CONSTRAINING_DIRECT_ENTRY_TARGET"
    return "REVIEWER"


def main() -> None:
    sources = sorted((ROOT / "reference-semantics").rglob("*.k"))
    sources.extend([ROOT / "verification.k", ROOT / "spec.k"])
    entries: list[Entry] = []
    for source in sources:
        entries.extend(logical_entries(source))

    tsv_path = EVIDENCE / "k-rule-inventory.tsv"
    with tsv_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, delimiter="\t", lineterminator="\n")
        writer.writerow(
            [
                "id",
                "role",
                "file",
                "start_line",
                "end_line",
                "kind",
                "attributes",
                "candidate_usage",
                "assessment",
                "logical_declaration",
            ]
        )
        for number, entry in enumerate(entries, start=1):
            writer.writerow(
                [
                    f"K{number:04d}",
                    role(entry.source),
                    entry.source.relative_to(ROOT).as_posix(),
                    entry.start,
                    entry.end,
                    entry.kind,
                    ",".join(tags(entry.text)),
                    usage(entry),
                    assessment(entry),
                    " ".join(line.strip() for line in entry.text.splitlines()),
                ]
            )

    counts: dict[tuple[str, str], int] = {}
    attribute_counts: dict[str, int] = {}
    usage_counts: dict[str, int] = {}
    for entry in entries:
        counts[(role(entry.source), entry.kind)] = (
            counts.get((role(entry.source), entry.kind), 0) + 1
        )
        usage_counts[usage(entry)] = usage_counts.get(usage(entry), 0) + 1
        for tag in tags(entry.text):
            attribute_counts[tag] = attribute_counts.get(tag, 0) + 1

    summary_path = EVIDENCE / "k-rule-inventory-summary.txt"
    with summary_path.open("w", encoding="utf-8") as output:
        output.write(f"source_count={len(sources)}\n")
        output.write(f"entry_count={len(entries)}\n")
        for key, count in sorted(counts.items()):
            output.write(f"count role={key[0]} kind={key[1]} value={count}\n")
        for key, count in sorted(usage_counts.items()):
            output.write(f"usage {key}={count}\n")
        reported_attributes = set(KNOWN_ATTRIBUTES) | set(attribute_counts)
        for key in sorted(reported_attributes):
            output.write(f"attribute {key}={attribute_counts.get(key, 0)}\n")
        output.write(f"inventory={tsv_path}\n")

    print(summary_path.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
