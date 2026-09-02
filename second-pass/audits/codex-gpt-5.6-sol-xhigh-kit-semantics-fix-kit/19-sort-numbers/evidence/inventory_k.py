#!/usr/bin/env python3
"""Create an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import pathlib
import re
import sys


START = re.compile(r"^\s*(configuration|syntax|rule|context)\b")
BOUNDARY = re.compile(r"^\s*(module|endmodule|imports|requires)\b")


USED_RULE_LINES = {
    "core.k": {
        69, 70, 97, 98, 101, 102, 108, 118, 125, 126, 127, 131, 132,
        152, 158, 189, 190, 191, 214, 215, 218, 219,
    },
    "call.k": {16, 20, 21, 24, 31, 38, 53, 56, 63, 69},
    "functions.k": {63, 64, 78, 85},
    "controls.k": {9},
    "tuple.k": {15, 16},
    "str.k": {14, 15, 16, 21, 22},
    "list.k": {19, 20},
    "methods.k": {26, 28, 29, 30, 72, 76, 77, 79, 83, 84, 86},
    "sort.k": {61},
}


def records(path: pathlib.Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    current: dict[str, object] | None = None
    for number, line in enumerate(lines, 1):
        match = START.match(line)
        if match:
            if current:
                yield current
            current = {"kind": match.group(1), "line": number, "parts": [line.strip()]}
        elif current and BOUNDARY.match(line):
            yield current
            current = None
        elif current:
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                current["parts"].append(stripped)  # type: ignore[index]
    if current:
        yield current


def attributes(text: str) -> str:
    names = [
        "function", "total", "functional", "no-evaluators", "concrete",
        "simplification", "owise", "macro-rec", "macro", "strict", "seqstrict",
    ]
    found = [name for name in names if re.search(rf"\b{re.escape(name)}\b", text)]
    priorities = re.findall(r"priority\(([^)]+)\)", text)
    found.extend(f"priority({value})" for value in priorities)
    return ",".join(found) if found else "-"


def disposition(path: pathlib.Path, kind: str, line: int, text: str) -> str:
    if path.name == "verification.k":
        return "LOCAL_REVIEWED_SOUND"
    if path.name == "concrete.k":
        return "CONCRETE_ONLY_REVIEWED_EVIDENCE"
    if "no-evaluators" in text:
        if path.name == "sort.k" and ("sortKeyVS" in text or "sortVS" in text):
            return "SUPPLIED_OPAQUE_SORT_TRUST_BOUNDARY"
        return "SUPPLIED_OPAQUE_UNUSED_BY_PROGRAM"
    if kind == "rule" and line in USED_RULE_LINES.get(path.name, set()):
        if path.name == "sort.k" and line == 61:
            return "USED_PATH_OPAQUE_SORT_DISPATCH"
        return "USED_PATH_REVIEWED_SOUND"
    if kind == "configuration" or (kind == "syntax" and path.name in {
        "syntax.k", "core.k", "call.k", "functions.k", "tuple.k", "str.k",
        "list.k", "methods.k", "sort.k",
    }):
        return "USED_DECLARATION_REVIEWED"
    return "SUPPLIED_BASELINE_UNUSED_NO_CANDIDATE_EFFECT"


def main() -> int:
    root = pathlib.Path(sys.argv[1])
    verification = pathlib.Path(sys.argv[2])
    paths = [root / "semantics.k", *sorted((root / "semantics").glob("*.k")), verification]
    counts: dict[str, int] = {}
    print("id\tfile\tline\tkind\tattributes\tdisposition\tdeclaration")
    item_id = 0
    for path in paths:
        for record in records(path):
            item_id += 1
            kind = str(record["kind"])
            line = int(record["line"])
            text = " ".join(record["parts"])  # type: ignore[arg-type]
            text = re.sub(r"\s+", " ", text).replace("\t", " ")
            counts[kind] = counts.get(kind, 0) + 1
            relative = (
                "verification.k"
                if path == verification
                else str(path.relative_to(root))
            )
            print(
                f"K{item_id:04d}\t{relative}\t{line}\t{kind}\t{attributes(text)}\t"
                f"{disposition(path, kind, line, text)}\t{text}"
            )
    print("SUMMARY", file=sys.stderr)
    for kind in sorted(counts):
        print(f"{kind}={counts[kind]}", file=sys.stderr)
    print(f"total={item_id}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
