#!/usr/bin/env python3
"""Create an exhaustive source-level inventory of local K declarations."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/tmp/audit-work/132-is-nested/source")
BASELINE = ROOT / "reference-semantics"
FILES = sorted(BASELINE.rglob("*.k")) + [ROOT / "verification.k", ROOT / "spec.k"]
START = re.compile(r"^\s{2}(configuration|syntax|rule|claim|context|alias)\b")
MODULE = re.compile(r"^\s*module\s+(\S+)")
ENDMODULE = re.compile(r"^\s*endmodule\b")
STRUCTURAL_BOUNDARY = re.compile(r"^\s*(?:module\s+\S+|endmodule|imports\s+\S+)\s*$")


@dataclass
class Item:
    path: Path
    module: str
    line: int
    kind: str
    text: str


def source_items(path: Path) -> list[Item]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str, str]] = []
    current_module = "(outside-module)"
    module_at_line: dict[int, str] = {}
    for index, line in enumerate(lines):
        module_match = MODULE.match(line)
        if module_match:
            current_module = module_match.group(1)
        module_at_line[index] = current_module
        start_match = START.match(line)
        if start_match:
            starts.append((index, start_match.group(1), current_module))
        if ENDMODULE.match(line):
            current_module = "(outside-module)"

    result: list[Item] = []
    for position, (index, kind, module_name) in enumerate(starts):
        end = len(lines)
        for candidate in range(index + 1, len(lines)):
            if START.match(lines[candidate]) or STRUCTURAL_BOUNDARY.match(lines[candidate]):
                end = candidate
                break
        while end > index and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
            or ENDMODULE.match(lines[end - 1])
        ):
            end -= 1
        result.append(
            Item(
                path=path,
                module=module_name,
                line=index + 1,
                kind=kind,
                text="\n".join(lines[index:end]),
            )
        )
    return result


def tags(item: Item) -> list[str]:
    text = item.text
    result = [item.kind]
    for tag in (
        "function",
        "functional",
        "total",
        "simplification",
        "priority",
        "owise",
        "no-evaluators",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(tag)}\b", text):
            result.append(tag)
    if "no-evaluators" in result:
        result.append("opaque")
    if item.kind == "rule" and "priority" not in result:
        result.append("ordinary-rule")
    return result


def disposition(item: Item) -> str:
    rel = item.path.relative_to(ROOT).as_posix()
    if rel.startswith("reference-semantics/"):
        if "no-evaluators" in item.text:
            return (
                "ACCEPTED TRUST BOUNDARY — opaque operation in the exact trusted "
                "supplied semantics; not on this program/proof path."
            )
        if item.kind == "syntax":
            return (
                "ACCEPTED BASELINE DECLARATION — exact trusted supplied syntax; "
                "task-path uses are mapped separately."
            )
        if item.kind == "configuration":
            return (
                "ACCEPTED BASELINE CONFIGURATION — exact trusted supplied cells; "
                "task-path cell effects are mapped separately."
            )
        return (
            "ACCEPTED RELATIVE TO SUPPLIED SEMANTICS — exact trusted baseline "
            "rule/context; unused rules add no candidate proof shortcut, and "
            "task-path rules receive a separate behavioral review."
        )
    if rel == "spec.k":
        return "CLAIM — adequacy and closure reviewed separately."
    line = item.line
    if line in (7, 26, 34):
        return "ACCEPTED exact translated-program definitional declaration."
    if line in (8, 27, 35):
        return "ACCEPTED exact translated-program definitional equation."
    if line == 39:
        return "ACCEPTED free bracket-sequence data constructors."
    if line == 43:
        return "REVIEWED proof-side symbolic string encoding declaration."
    if line in (44, 45, 47):
        return "REVIEWED operational iterator bridge for the symbolic encoding."
    if line in (51, 55, 59, 64):
        return "ACCEPTED total mathematical-summary declaration."
    if line in (52, 56, 60, 61, 62, 65):
        return "ACCEPTED truthful, terminating mathematical-summary equation."
    if line == 74:
        return (
            "REJECTED operational bridge — its _REST:Map match domain is broader "
            "than the proved loop claim's fixed global/builtins scopes."
        )
    return "REQUIRES MANUAL CLASSIFICATION."


def main() -> int:
    inventory: list[Item] = []
    for path in FILES:
        inventory.extend(source_items(path))
    counts: dict[str, int] = {}
    tag_counts: dict[str, int] = {}
    for item in inventory:
        counts[item.kind] = counts.get(item.kind, 0) + 1
        for tag in tags(item):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    print("# Exhaustive K source inventory")
    print()
    print(
        "This inventory covers every source-level `configuration`, `syntax`, "
        "`rule`, `claim`, `context`, and `alias` statement in the clean trusted "
        "supplied-semantics copy plus `verification.k` and `spec.k`."
    )
    print()
    print(f"- Files: {len(FILES)}")
    print(f"- Items: {len(inventory)}")
    print(f"- Kind counts: `{counts}`")
    print(f"- Attribute/class counts: `{tag_counts}`")
    print(
        "- No omitted local simplification rules: the count above is zero when "
        "`simplification` is absent."
    )
    print()
    for number, item in enumerate(inventory, 1):
        rel = item.path.relative_to(ROOT).as_posix()
        item_tags = ", ".join(tags(item))
        print(f"## K-{number:04d} — `{rel}:{item.line}`")
        print()
        print(f"- Module: `{item.module}`")
        print(f"- Class/tags: `{item_tags}`")
        print(f"- Disposition: {disposition(item)}")
        print()
        print("```k")
        print(item.text)
        print("```")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
