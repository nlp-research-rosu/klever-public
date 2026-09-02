#!/usr/bin/env python3
"""Build an exhaustive, line-addressed inventory of K declarations and rules."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/27-flip-case/candidate")
OUTPUT = Path("/audit-output/evidence/rule-inventory.md")
START = re.compile(r"^\s{2}(syntax|rule|claim|context|configuration)\b")
BOUNDARY = re.compile(
    r"^\s{0,2}(?:syntax|rule|claim|context|configuration|endmodule|module)\b"
)
BRACKET = re.compile(r"\[([^\]]+)\]")
ATTRIBUTE_TOKEN = re.compile(
    r"(?:"
    r"macro-rec|macro|function|functional|total|simplification|owise|concrete|"
    r"no-evaluators|priority\(\d+\)|symbol\([^)]*\)|"
    r"seqstrict\([^)]*\)|strict(?:\([^)]*\))?"
    r")"
)


def relevant(path: Path, line: int) -> bool:
    name = path.name
    ranges = {
        "syntax.k": [(9, 30), (41, 61)],
        "core.k": [(13, 60), (124, 191), (213, 219)],
        "functions.k": [(8, 20), (62, 91)],
        "call.k": [(15, 24), (69, 75)],
        "methods.k": [(10, 21), (112, 164)],
    }
    return any(start <= line <= end for start, end in ranges.get(name, []))


def decision(path: Path, line: int, text: str, attrs: list[str]) -> str:
    if path.name == "verification.k":
        if line in (8, 9):
            return "ACCEPTED_LOCAL: exact alias for the submitted function body"
        if line in (12, 13):
            return "ACCEPTED_LOCAL: exact alias for the submitted Module constructor tree"
        if line == 21:
            return "ACCEPTED_LOCAL: fresh runner syntax only"
        if line == 22:
            return (
                "ACCEPTED_LOCAL: setup rule expands to real module load and call; "
                "does not replace function execution"
            )
        return "REVIEWED_LOCAL"
    if path.name == "spec.k":
        return "TARGET_CLAIM: result-constraining entry theorem, audited separately"
    joined_attrs = ",".join(attrs)
    if "no-evaluators" in joined_attrs or (
        "symbol(" in joined_attrs and "[concrete]" not in text
    ):
        return "UNUSED_TRUST_BOUNDARY: opaque/partly opaque supplied primitive, unreachable here"
    if path.name == "methods.k" and 112 <= line <= 164:
        return (
            "ACCEPTED_IN_SUPPLIED_ASCII_MODEL: truthful and exhaustive there; "
            "not a universal model of Python Unicode casing"
        )
    if relevant(path, line):
        return "ACCEPTED_REACHABLE_BASELINE: inspected in the real execution slice"
    return (
        "SUPPLIED_BASELINE_OUTSIDE_SLICE: no constructor/symbol overlap with "
        "the submitted program's reachable execution"
    )


def statements(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    result: list[dict[str, object]] = []
    for position, start in enumerate(starts):
        end_limit = starts[position + 1] if position + 1 < len(starts) else len(lines)
        end = end_limit
        for index in range(start + 1, end_limit):
            if BOUNDARY.match(lines[index]):
                end = index
                break
        while end > start + 1 and (
            not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        text = "\n".join(lines[start:end]).rstrip()
        match = START.match(lines[start])
        assert match is not None
        raw_attrs = [
            token
            for group in BRACKET.findall(text)
            for token in ATTRIBUTE_TOKEN.findall(group)
        ]
        result.append(
            {
                "path": path,
                "line": start + 1,
                "end_line": end,
                "kind": match.group(1),
                "text": text,
                "attrs": raw_attrs,
            }
        )
    return result


def main() -> int:
    paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
    paths.extend([ROOT / "verification.k", ROOT / "spec.k"])
    inventory = [statement for path in paths for statement in statements(path)]
    counts = collections.Counter(str(item["kind"]) for item in inventory)
    attr_counts: collections.Counter[str] = collections.Counter()
    for item in inventory:
        for attribute in item["attrs"]:  # type: ignore[union-attr]
            attr_counts[str(attribute)] += 1

    with OUTPUT.open("w", encoding="utf-8") as stream:
        stream.write("# Exhaustive K declaration and rule inventory\n\n")
        stream.write(
            "Generated from the clean scratch source tree. Every source-level "
            "`syntax`, `configuration`, `context`, `rule`, and `claim` directive "
            "is listed exactly once. K built-in modules are outside this local inventory.\n\n"
        )
        stream.write("## Summary\n\n")
        stream.write(f"- Files: {len(paths)}\n")
        stream.write(f"- Directives: {len(inventory)}\n")
        for key in sorted(counts):
            stream.write(f"- {key}: {counts[key]}\n")
        stream.write("- Attribute tokens: `" + json.dumps(dict(sorted(attr_counts.items()))) + "`\n\n")

        for ordinal, item in enumerate(inventory, 1):
            path = item["path"]
            assert isinstance(path, Path)
            rel = path.relative_to(ROOT).as_posix()
            line = int(item["line"])
            end_line = int(item["end_line"])
            attrs = item["attrs"]
            assert isinstance(attrs, list)
            text = str(item["text"])
            stream.write(f"## K{ordinal:04d} — `{rel}:{line}-{end_line}`\n\n")
            stream.write(f"- Kind: `{item['kind']}`\n")
            stream.write(f"- Attributes: `{', '.join(str(value) for value in attrs) or 'none'}`\n")
            stream.write(f"- Reachable slice: `{'yes' if relevant(path, line) or path.name in {'verification.k', 'spec.k'} else 'no'}`\n")
            stream.write(f"- Decision: {decision(path, line, text, attrs)}\n\n")
            stream.write("```k\n")
            stream.write(text + "\n")
            stream.write("```\n\n")

    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "files": len(paths),
                "directives": len(inventory),
                "kind_counts": dict(sorted(counts.items())),
                "attribute_counts": dict(sorted(attr_counts.items())),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
