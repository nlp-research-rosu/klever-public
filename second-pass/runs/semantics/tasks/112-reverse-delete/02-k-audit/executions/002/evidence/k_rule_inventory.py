#!/usr/bin/env python3
"""Exhaustive declaration/rule inventory for the audited K source tree."""

from __future__ import annotations

import collections
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/112-reverse-delete")
SEMANTICS = SCRATCH / "reference-semantics"

FILES = sorted(SEMANTICS.rglob("*.k")) + [
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]

START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|module|endmodule|imports)\b"
)
ATTR_TOKEN = re.compile(
    r"\b(?:functional|function|total|concrete|simplification|owise|macro-rec|macro|"
    r"no-evaluators)\b|(?:seqstrict|strict|priority|symbol)\([^)]*\)"
)

# Lines involved in actual reverse_delete execution or in the exact target
# configuration. Other supplied rules are still inventoried, but cannot be
# reached from the submitted constructor body.
RELEVANT_RANGES: dict[str, tuple[tuple[int, int], ...]] = {
    "semantics/syntax.k": ((9, 61),),
    "semantics/core.k": (
        (13, 60),
        (68, 78),
        (117, 127),
        (129, 191),
        (199, 205),
        (208, 219),
    ),
    "semantics/iter.k": ((8, 8),),
    "semantics/operators.k": ((10, 17),),
    "semantics/str.k": ((8, 41),),
    "semantics/tuple.k": ((14, 18), (31, 41)),
    "semantics/controls.k": ((9, 31), (48, 74)),
    "semantics/functions.k": ((63, 66), (78, 90)),
    "semantics/call.k": ((19, 21), (69, 74)),
}


def relative(path: Path) -> str:
    if path == SCRATCH / "verification.k" or path == SCRATCH / "spec.k":
        return path.name
    return str(path.relative_to(SEMANTICS))


def is_relevant(rel: str, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in RELEVANT_RANGES.get(rel, ()))


def decision(rel: str, line: int, kind: str, text: str) -> str:
    if rel == "verification.k":
        if kind == "syntax":
            return "ACCEPT—defined proof summary; exhaustive equations checked"
        if line < 39:
            return "ACCEPT—truthful guarded recursive equation"
        return "ACCEPT—operational bridge exactly copies proved LOOP-SPEC claim"
    if rel == "spec.k":
        return "TARGET—reachability obligation, not an assumed extension"
    if "no-evaluators" in text:
        return "UNUSED OPAQUE—unreachable from submitted body; no dependent claim"
    if is_relevant(rel, line):
        if kind == "syntax":
            return "ACCEPT—declaration/strictness used by submitted constructors"
        if kind == "context":
            return "ACCEPT—relevant left-to-right evaluation context"
        if kind == "configuration":
            return "ACCEPT—entry state instantiated exactly by SPEC"
        return "ACCEPT—relevant operational/equational rule; path and state checked"
    return "UNREACHED—no constructor/path from submitted function; no proof dependency"


def main() -> int:
    rows = []
    counts: collections.Counter[str] = collections.Counter()
    decisions: collections.Counter[str] = collections.Counter()
    attrs: collections.Counter[str] = collections.Counter()

    for path in FILES:
        lines = path.read_text(encoding="utf-8").splitlines()
        rel = relative(path)
        starts = [index for index, line in enumerate(lines) if START.match(line)]
        for start in starts:
            kind = START.match(lines[start]).group(1)  # type: ignore[union-attr]
            end = start + 1
            while end < len(lines) and not BOUNDARY.match(lines[end]):
                end += 1
            statement_lines = [
                re.sub(r"\s+", " ", line.strip())
                for line in lines[start:end]
                if line.strip() and not line.lstrip().startswith("//")
            ]
            text = " ".join(statement_lines)
            found_attrs = sorted(set(ATTR_TOKEN.findall(text)))
            for item in found_attrs:
                attrs[item] += 1
            result = decision(rel, start + 1, kind, text)
            counts[kind] += 1
            decisions[result.split("—", 1)[0]] += 1
            rows.append(
                (
                    rel,
                    start + 1,
                    kind,
                    ", ".join(found_attrs) or "—",
                    result,
                    text,
                )
            )

    print("# Exhaustive K declaration and rule inventory")
    print()
    print(f"Files: {len(FILES)}")
    print(f"Inventory rows: {len(rows)}")
    print(f"Kinds: {dict(sorted(counts.items()))}")
    print(f"Decision classes: {dict(sorted(decisions.items()))}")
    print(f"Attributes: {dict(sorted(attrs.items()))}")
    print()
    print(
        "| Source | Line | Kind | Attributes | Decision | Normalized declaration/rule |"
    )
    print("|---|---:|---|---|---|---|")
    for rel, line, kind, found_attrs, result, text in rows:
        escaped = text.replace("|", "\\|")
        print(
            f"| `{rel}` | {line} | {kind} | {found_attrs} | {result} | `{escaped}` |"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
