#!/usr/bin/env python3
"""Create a complete source-level K declaration/rule inventory for this audit."""

from __future__ import annotations

import re
from pathlib import Path


WORK = Path("/tmp/audit-work/50-decode-shift")
SEMANTICS = WORK / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")

START = re.compile(r"^\s*(syntax|rule|claim|context|configuration)\b")
BOUNDARY = re.compile(
    r"^\s*(syntax|rule|claim|context|configuration|module|endmodule|requires|imports)\b"
)

ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "concrete",
    "simplification",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)

MATERIAL_STARTS: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {
        9,
        41,
        56,
        57,
        60,
        61,
    },
    "reference-semantics/semantics/core.k": {
        13,
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
        210,
        213,
        214,
        215,
    },
    "reference-semantics/semantics/iter.k": {8},
    "reference-semantics/semantics/int.k": {9, 13, 15, 19, 20},
    "reference-semantics/semantics/str.k": {
        8,
        9,
        13,
        14,
        15,
        16,
        20,
        21,
        22,
        24,
    },
    "reference-semantics/semantics/operators.k": {12},
    "reference-semantics/semantics/controls.k": {
        9,
        48,
        65,
        69,
        71,
        72,
        73,
    },
    "reference-semantics/semantics/functions.k": {
        8,
        14,
        63,
        64,
        78,
        80,
        85,
    },
    "reference-semantics/semantics/call.k": {19, 20, 21, 31, 69},
    "reference-semantics/semantics/tuple.k": {31, 32},
    "reference-semantics/semantics/builtins.k": {17, 143, 144},
}


def strip_comment(line: str) -> str:
    in_string = False
    escaped = False
    index = 0
    while index + 1 < len(line):
        char = line[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "/" and line[index + 1] == "/":
            return line[:index]
        index += 1
    return line


def statements(path: Path):
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines):
            if BOUNDARY.match(lines[index]):
                break
            index += 1
        raw = "\n".join(lines[start:index])
        clean = "\n".join(strip_comment(line) for line in raw.splitlines())
        clean = " ".join(clean.split())
        yield start + 1, kind, clean


def role(kind: str, text: str) -> str:
    if kind == "syntax":
        return "syntax-declaration"
    if kind == "context":
        return "evaluation-context"
    if kind == "configuration":
        return "configuration"
    if kind == "claim":
        return "reachability-claim"
    if "<k>" in text:
        return "operational-rule"
    if any(name in text for name in ("compBody(", "compNest(", "compGuard(")):
        return "macro-equation"
    return "function-equation"


def attributes(text: str) -> str:
    attribute_text = " ".join(re.findall(r"\[([^\[\]]*)\]", text))
    found = []
    for attribute in ATTRIBUTES:
        if re.search(
            rf"(?<![A-Za-z0-9-]){re.escape(attribute)}(?![A-Za-z0-9-])",
            attribute_text,
        ):
            found.append(attribute)
    priority = re.search(r"priority\(([^)]+)\)", attribute_text)
    if priority:
        found = [item for item in found if item != "priority"]
        found.append(f"priority({priority.group(1)})")
    return ",".join(found) if found else "-"


def influence(path: Path, line: int) -> str:
    if path.name == "verification.k":
        return "PROOF_LOCAL"
    if path.name == "spec.k":
        return "CLAIM"
    if "semantics/concrete.k" in path.as_posix():
        return "LLVM_ONLY_UNUSED"
    relative = path.relative_to(WORK).as_posix()
    return (
        "MATERIAL_PATH"
        if line in MATERIAL_STARTS.get(relative, set())
        else "IMPORTED_UNUSED"
    )


def assessment(path: Path, kind: str, attrs: str, effect: str) -> str:
    if path.name == "verification.k":
        return "ACCEPTABLE_REVIEWED_DEFINITION"
    if path.name == "spec.k":
        return "ACCEPTABLE_RECONSTRUCTED_CLAIM"
    if effect == "MATERIAL_PATH":
        return "ACCEPTABLE_REVIEWED_FIXED_PATH"
    if effect == "LLVM_ONLY_UNUSED":
        return "ACCEPTABLE_CONCRETE_ONLY_UNUSED"
    if "no-evaluators" in attrs:
        return "ACCEPTABLE_TRUSTED_OPAQUE_UNUSED"
    return "ACCEPTABLE_FIXED_SEMANTICS_UNUSED"


def main() -> None:
    paths = [
        SEMANTICS / "semantics.k",
        *sorted((SEMANTICS / "semantics").glob("*.k")),
        WORK / "verification.k",
        WORK / "spec.k",
    ]
    rows = []
    for path in paths:
        for line, kind, text in statements(path):
            attrs = attributes(text)
            effect = influence(path, line)
            rows.append(
                (
                    str(len(rows) + 1),
                    path.relative_to(WORK).as_posix(),
                    str(line),
                    kind,
                    role(kind, text),
                    attrs,
                    effect,
                    assessment(path, kind, attrs, effect),
                    text,
                )
            )

    header = (
        "id",
        "file",
        "line",
        "kind",
        "role",
        "attributes",
        "influence",
        "assessment",
        "source",
    )
    with OUTPUT.open("w", encoding="utf-8") as stream:
        stream.write("\t".join(header) + "\n")
        for row in rows:
            stream.write("\t".join(field.replace("\t", " ") for field in row) + "\n")

    counts: dict[str, int] = {}
    for row in rows:
        for key in (
            f"kind={row[3]}",
            f"role={row[4]}",
            f"influence={row[6]}",
            f"assessment={row[7]}",
        ):
            counts[key] = counts.get(key, 0) + 1
    print(f"INVENTORY_PATH {OUTPUT}")
    print(f"INVENTORY_ROWS {len(rows)}")
    for key in sorted(counts):
        print(f"COUNT {key} {counts[key]}")
    print(
        "SPECIAL_COUNTS "
        f"function={sum('function' in row[5].split(',') for row in rows)} "
        f"total={sum('total' in row[5].split(',') for row in rows)} "
        f"functional={sum('functional' in row[5].split(',') for row in rows)} "
        f"opaque={sum('no-evaluators' in row[5].split(',') for row in rows)} "
        f"priority={sum('priority(' in row[5] for row in rows)} "
        f"simplification={sum('simplification' in row[5].split(',') for row in rows)}"
    )
    print("K_INVENTORY PASS")


if __name__ == "__main__":
    main()
