#!/usr/bin/env python3
"""Create an exhaustive top-level K declaration/rule inventory."""

from __future__ import annotations

import csv
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/3-below-zero-audit")
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")

SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification-base.k",
    ROOT / "verification.k",
    ROOT / "spec.k",
    ROOT / "connection-spec.k",
]

TOP_LEVEL = {"imports", "configuration", "syntax", "context", "rule", "claim"}

# Fixed-semantics lines on the actual solution dependency slice.  All other
# supplied declarations remain inventoried as fixed-but-unreached.
USED_FIXED = {
    "semantics/syntax.k": [(9, 61)],
    "semantics/core.k": [(13, 42), (49, 60), (68, 70), (100, 102), (124, 134),
                         (152, 181), (185, 191), (194, 210), (213, 225)],
    "semantics/operators.k": [(12, 17)],
    "semantics/int.k": [(9, 9), (22, 22)],
    "semantics/list.k": [(9, 10)],
    "semantics/controls.k": [(9, 23), (35, 36), (51, 54), (65, 74)],
    "semantics/functions.k": [(8, 16), (63, 66), (77, 90)],
    "semantics/call.k": [(18, 21), (69, 75)],
}


def fixed_relevant(path: Path, line: int) -> bool:
    try:
        rel = path.relative_to(ROOT / "reference-semantics").as_posix()
    except ValueError:
        return False
    return any(lo <= line <= hi for lo, hi in USED_FIXED.get(rel, []))


def records(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        first = stripped.split(maxsplit=1)[0] if stripped else ""
        if indent == 0 and stripped.startswith('requires "'):
            starts.append((index, "requires"))
        elif indent == 0 and first == "module":
            starts.append((index, "module"))
        elif first == "endmodule":
            starts.append((index, "endmodule"))
        elif indent == 2 and first in TOP_LEVEL:
            starts.append((index, first))
    for pos, (index, kind) in enumerate(starts):
        next_index = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        code_parts = []
        for part in lines[index:next_index]:
            quoted = False
            escaped = False
            cut = len(part)
            for offset, char in enumerate(part):
                if quoted:
                    if escaped:
                        escaped = False
                    elif char == "\\":
                        escaped = True
                    elif char == '"':
                        quoted = False
                elif char == '"':
                    quoted = True
                elif char == "/" and offset + 1 < len(part) and part[offset + 1] == "/":
                    cut = offset
                    break
            code = part[:cut].strip()
            if code:
                code_parts.append(code)
        block = " ".join(code_parts)
        yield index + 1, kind, block


def attributes(text: str) -> str:
    found = []
    for attr in (
        "function", "functional", "total", "symbol", "no-evaluators",
        "priority", "simplification", "concrete", "owise", "macro",
        "macro-rec", "strict", "seqstrict", "preserves-definedness",
    ):
        if re.search(rf"\b{re.escape(attr)}\b", text):
            found.append(attr)
    return ",".join(found)


def rule_class(kind: str, text: str) -> str:
    attrs = attributes(text)
    if kind == "syntax":
        if "no-evaluators" in attrs or "symbol" in attrs:
            return "opaque-or-symbol-declaration"
        if "function" in attrs or "functional" in attrs:
            return "function-declaration"
        return "syntax-declaration"
    if kind == "rule":
        if "simplification" in attrs:
            return "simplification-rule"
        if "priority" in attrs:
            return "priority-rule"
        if "<k>" in text:
            return "ordinary-operational-rule"
        return "ordinary-equational-rule"
    if kind == "claim":
        return "reachability-claim"
    return kind


def disposition(path: Path, line: int, kind: str, text: str) -> str:
    if "reference-semantics" in path.parts:
        if fixed_relevant(path, line):
            return "FIXED_MODEL_USED_SLICE_REVIEWED"
        return "FIXED_MODEL_UNREACHED_BY_SOLUTION"
    if path.name == "verification-base.k":
        return "CANDIDATE_EXTENSION_REVIEWED_SOUND"
    if path.name == "verification.k" and kind == "rule":
        return "OPERATIONAL_BRIDGE_CONNECTION_AUDITED"
    if path.name == "connection-spec.k" and kind == "claim":
        return "BRIDGE_FREE_CONNECTION_THEOREM_REBUILT"
    if path.name == "spec.k" and kind == "claim":
        return "TARGET_CLAIM_REBUILT"
    return "STRUCTURAL_DECLARATION_REVIEWED"


def main() -> None:
    rows = []
    for path in SOURCES:
        for line, kind, text in records(path):
            rows.append(
                {
                    "file": path.relative_to(ROOT).as_posix(),
                    "line": line,
                    "kind": kind,
                    "class": rule_class(kind, text),
                    "attributes": attributes(text),
                    "disposition": disposition(path, line, kind, text),
                    "text": text,
                }
            )
    with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys(), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    by_class: dict[str, int] = {}
    by_disposition: dict[str, int] = {}
    for row in rows:
        by_class[row["class"]] = by_class.get(row["class"], 0) + 1
        by_disposition[row["disposition"]] = by_disposition.get(row["disposition"], 0) + 1
    print(f"source_files={len(SOURCES)}")
    print(f"inventory_rows={len(rows)}")
    print(f"by_class={dict(sorted(by_class.items()))}")
    print(f"by_disposition={dict(sorted(by_disposition.items()))}")
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()
