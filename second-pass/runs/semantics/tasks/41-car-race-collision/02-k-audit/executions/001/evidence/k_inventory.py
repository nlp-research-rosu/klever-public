#!/usr/bin/env python3
from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction/work")
OUTPUT = Path("/audit-output/evidence/k-rule-inventory.tsv")
PATH_OUTPUT = Path("/audit-output/evidence/k-program-path-inventory.tsv")

SOURCE_FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(r"^\s*(configuration|syntax|context|rule|claim|alias)\b")
STOP = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|alias|module|endmodule|imports)\b"
)

# Source lines on the submitted program's actual execution/proof path. Syntax
# declarations include generated strictness/heating/cooling for used nodes.
USED_LINES: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 37, 41, 53, 56, 57, 60, 61},
    "semantics/core.k": {
        25,
        31,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        152,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        194,
        208,
        209,
        213,
        214,
    },
    "semantics/functions.k": {8, 14, 63, 64, 78, 85},
    "semantics/call.k": {19, 20, 21, 69},
    "semantics/operators.k": {12},
    "semantics/int.k": {14},
    "verification.k": {7, 8, 14, 15},
    "spec.k": {6},
}


def relative_name(path: Path) -> str:
    reference_root = ROOT / "reference-semantics"
    if path.is_relative_to(reference_root):
        return str(path.relative_to(reference_root))
    return path.name


def entities(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end = len(lines)
        for later in range(start + 1, len(lines)):
            if STOP.match(lines[later]):
                end = later
                break
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        yield start + 1, "\n".join(block_lines)


def classify(block: str) -> tuple[str, list[str]]:
    first = block.lstrip().split(None, 1)[0]
    code_only = "\n".join(line.split("//", 1)[0] for line in block.splitlines())
    tags: list[str] = []
    for tag in [
        "function",
        "functional",
        "total",
        "macro-rec",
        "macro",
        "no-evaluators",
        "concrete",
        "simplification",
        "owise",
        "priority",
        "strict",
        "seqstrict",
        "symbol",
    ]:
        if re.search(rf"\b{re.escape(tag)}\b", code_only):
            tags.append(tag)
    return first, tags


def main() -> int:
    records = []
    for path in SOURCE_FILES:
        rel = relative_name(path)
        used_lines = USED_LINES.get(rel, set())
        for line, block in entities(path):
            entity_class, tags = classify(block)
            used = line in used_lines
            if rel == "verification.k":
                disposition = "PROOF_LOCAL_USED_EXACT" if used else "PROOF_LOCAL_REVIEWED"
            elif rel == "spec.k":
                disposition = "TARGET_CLAIM_REVIEWED"
            elif used:
                disposition = "FIXED_USED_PATH_ACCEPTED"
            elif "no-evaluators" in tags:
                disposition = "FIXED_OPAQUE_UNUSED"
            elif "concrete" in tags:
                disposition = "FIXED_CONCRETE_ONLY_UNUSED"
            elif "total" in tags:
                disposition = "FIXED_TOTAL_UNUSED"
            else:
                disposition = "FIXED_UNUSED_REVIEWED"
            normalized = " ".join(part.strip() for part in block.splitlines())
            records.append(
                (
                    rel,
                    line,
                    entity_class,
                    ",".join(tags) if tags else "-",
                    "YES" if used else "NO",
                    disposition,
                    normalized,
                )
            )

    with OUTPUT.open("w", encoding="utf-8") as handle:
        handle.write(
            "file\tline\tentity\ttags\tprogram_path\tdisposition\tdeclaration_or_rule\n"
        )
        for record in records:
            handle.write("\t".join(map(str, record)) + "\n")
    with PATH_OUTPUT.open("w", encoding="utf-8") as handle:
        handle.write(
            "file\tline\tentity\ttags\tprogram_path\tdisposition\tdeclaration_or_rule\n"
        )
        for record in records:
            if record[4] == "YES":
                handle.write("\t".join(map(str, record)) + "\n")

    by_entity = collections.Counter(record[2] for record in records)
    by_file = collections.Counter(record[0] for record in records)
    by_tag = collections.Counter(
        tag for record in records for tag in record[3].split(",") if tag != "-"
    )
    print(f"inventory_path={OUTPUT}")
    print(f"program_path_inventory={PATH_OUTPUT}")
    print(f"source_file_count={len(SOURCE_FILES)}")
    print(f"entity_count={len(records)}")
    print("entity_counts=" + ",".join(f"{key}:{by_entity[key]}" for key in sorted(by_entity)))
    print("tag_counts=" + ",".join(f"{key}:{by_tag[key]}" for key in sorted(by_tag)))
    for file_name in sorted(by_file):
        print(f"file_count {file_name} {by_file[file_name]}")
    print(f"program_path_entity_count={sum(record[4] == 'YES' for record in records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
