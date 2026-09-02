#!/usr/bin/env python3
"""Build a complete declaration/rule inventory for the audited K source."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/connection-spec.k"),
]

ITEM_START = re.compile(
    r"^\s*(syntax|configuration|context|rule|claim)\b"
)
MODULE_START = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")

# Material declarations/rules used by the submitted solution's target proof.
# Lines refer to the immutable trusted semantics mount.
USED_FIXED: dict[str, set[int]] = {
    "syntax.k": set(range(9, 63)),
    "core.k": {
        13,
        14,
        15,
        18,
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        68,
        69,
        70,
        124,
        125,
        126,
        127,
        130,
        131,
        132,
        145,
        152,
        157,
        158,
        185,
        186,
        189,
        190,
        191,
        196,
        199,
        201,
        204,
        208,
        210,
        213,
        214,
        215,
        217,
        218,
        219,
        223,
        224,
        225,
        227,
        228,
        229,
    },
    "iter.k": {8},
    "bool.k": {8},
    "operators.k": {10, 15, 16, 17},
    "int.k": {24},
    "list.k": {9, 10},
    "tuple.k": {31, 32},
    "subscript.k": {11, 12, 13, 21, 22, 23, 27, 28, 35, 37, 38},
    "controls.k": {9, 36, 51, 52, 53, 54, 65, 69, 71, 72, 73},
    "functions.k": {8, 14, 63, 64, 78, 80, 85},
    "call.k": {19, 20, 21, 31, 69},
    "builtins.k": {17, 20, 21, 24},
}


def flatten(block: list[str]) -> str:
    uncommented = []
    for line in block:
        code = line.split("//", 1)[0]
        if re.match(r"^\s*(module|endmodule|imports)\b", code):
            continue
        uncommented.append(code)
    return " ".join(
        part for line in uncommented for part in line.strip().split()
    ).replace("\t", " ")


def flags(text: str) -> list[str]:
    attributes = " ".join(re.findall(r"\[([^\]]+)\]", text))
    found = []
    for flag, marker in [
        ("function", "function"),
        ("total", "total"),
        ("functional", "functional"),
        ("symbol", "symbol("),
        ("opaque", "no-evaluators"),
        ("priority", "priority("),
        ("simplification", "simplification"),
        ("concrete", "concrete"),
        ("symbolic", "symbolic("),
        ("owise", "owise"),
        ("macro", "macro"),
        ("strict", "strict"),
    ]:
        if marker in attributes:
            found.append(flag)
    return found


def decision(path: Path, line: int, kind: str, item_flags: list[str]) -> str:
    if path == Path("/candidate/verification.k"):
        if kind == "rule":
            return "REVIEWED_SOUND_PROOF_EXTENSION"
        return "REVIEWED_WELL_SORTED_PROOF_DECLARATION"
    if path == Path("/candidate/spec.k"):
        if kind == "claim":
            return "REVIEWED_SOUND_REACHABILITY_CLAIM"
        return "REVIEWED_WELL_SORTED_SPEC_DECLARATION"
    if path == Path("/candidate/connection-spec.k"):
        if kind == "claim":
            return "REVIEWED_SOUND_SUPPORTING_CLAIM"
        return "REVIEWED_WELL_SORTED_CONNECTION_DECLARATION"

    used = line in USED_FIXED.get(path.name, set())
    if used:
        if kind == "rule":
            return "SOUND_ON_REAL_PROGRAM_PATH"
        return "MATERIAL_FIXED_DECLARATION_REVIEWED"
    if "opaque" in item_flags:
        return "UNEXERCISED_FIXED_OPAQUE_BOUNDARY"
    if kind == "rule":
        return "UNEXERCISED_NO_INTENDED_DOMAIN_FALSE_WITNESS"
    return "UNEXERCISED_FIXED_DECLARATION"


def main() -> None:
    records: list[dict[str, object]] = []
    for path in ROOTS:
        lines = path.read_text(encoding="utf-8").splitlines()
        module = "<outside-module>"
        starts: list[tuple[int, str, str]] = []
        for index, line in enumerate(lines, 1):
            module_match = MODULE_START.match(line)
            if module_match:
                module = module_match.group(1)
            item_match = ITEM_START.match(line)
            if item_match:
                starts.append((index, item_match.group(1), module))
        for ordinal, (line, kind, item_module) in enumerate(starts):
            end = starts[ordinal + 1][0] - 1 if ordinal + 1 < len(starts) else len(lines)
            block = lines[line - 1 : end]
            text = flatten(block)
            item_flags = flags(text)
            records.append(
                {
                    "path": str(path),
                    "line": line,
                    "module": item_module,
                    "kind": kind,
                    "flags": ",".join(item_flags) if item_flags else "-",
                    "decision": decision(path, line, kind, item_flags),
                    "text": text,
                }
            )

    output = Path("/audit-output/evidence/static-rule-inventory.tsv")
    with output.open("w", encoding="utf-8") as stream:
        stream.write("path\tline\tmodule\tkind\tflags\tdecision\ttext\n")
        for record in records:
            stream.write(
                "\t".join(str(record[key]) for key in (
                    "path",
                    "line",
                    "module",
                    "kind",
                    "flags",
                    "decision",
                    "text",
                ))
                + "\n"
            )

    kind_counts = Counter(str(record["kind"]) for record in records)
    decision_counts = Counter(str(record["decision"]) for record in records)
    flag_counts: Counter[str] = Counter()
    for record in records:
        for flag in str(record["flags"]).split(","):
            if flag != "-":
                flag_counts[flag] += 1

    summary = Path("/audit-output/evidence/static-rule-inventory-summary.txt")
    with summary.open("w", encoding="utf-8") as stream:
        stream.write(f"records={len(records)}\n")
        stream.write(f"kinds={dict(sorted(kind_counts.items()))}\n")
        stream.write(f"flags={dict(sorted(flag_counts.items()))}\n")
        stream.write(f"decisions={dict(sorted(decision_counts.items()))}\n")
        stream.write("source_files:\n")
        for path in ROOTS:
            count = sum(1 for record in records if record["path"] == str(path))
            stream.write(f"  {path}: {count}\n")

    print(summary.read_text(encoding="utf-8"), end="")
    print(f"inventory={output}")


if __name__ == "__main__":
    main()
