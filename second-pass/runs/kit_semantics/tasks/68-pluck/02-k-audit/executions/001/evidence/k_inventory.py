#!/usr/bin/env python3
"""Generate a source-ordered exhaustive declaration/rule inventory."""

from __future__ import annotations

import collections
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/68-pluck")
OUTPUT = Path("/audit-output/evidence/k-rule-inventory.md")
SOURCE_FILES = [
    WORK / "reference-semantics" / "semantics.k",
    *sorted((WORK / "reference-semantics" / "semantics").glob("*.k")),
    WORK / "verification.k",
    WORK / "spec.k",
]
START = re.compile(
    r"^(?:(requires)\b|\s*(module|imports|syntax|configuration|context|rule|claim|priority|endmodule)\b)"
)


def declarations(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = lines[start:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        yield start + 1, start + len(block), kind, "\n".join(block)


def tags(kind: str, block: str) -> list[str]:
    code = "\n".join(line.split("//", 1)[0] for line in block.splitlines())
    result: list[str] = []
    if kind == "syntax":
        for tag in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "macro-rec",
            "macro",
            "token",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(tag)}\b", code):
                result.append(tag)
        if "no-evaluators" in code:
            result.append("opaque")
    elif kind == "rule":
        result.append("operational" if "<k>" in code else "pure/equational")
        if "simplification" in code:
            result.append("simplification")
        else:
            result.append("ordinary")
        for tag in (
            "priority",
            "owise",
            "concrete",
            "symbolic",
            "preserves-definedness",
            "macro-rec",
            "macro",
            "anywhere",
        ):
            if re.search(rf"\b{re.escape(tag)}\b", code):
                result.append(tag)
    elif kind == "claim":
        result.append("reachability-claim")
    return result


def main() -> None:
    totals: collections.Counter[str] = collections.Counter()
    per_file: dict[str, collections.Counter[str]] = {}
    rendered: list[str] = []
    for path in SOURCE_FILES:
        relative = path.relative_to(WORK).as_posix()
        counter: collections.Counter[str] = collections.Counter()
        entries = list(declarations(path))
        for _start, _end, kind, block in entries:
            counter[kind] += 1
            totals[kind] += 1
            for tag in tags(kind, block):
                counter[tag] += 1
                totals[tag] += 1
        per_file[relative] = counter

        rendered.append(f"## `{relative}`\n")
        for start, end, kind, block in entries:
            classification = ", ".join(tags(kind, block)) or "structural/module"
            span = f"{start}" if start == end else f"{start}-{end}"
            normalized = " ".join(
                line.strip() for line in block.splitlines() if line.strip()
            )
            rendered.append(
                f"- `{relative}:{span}` — **{kind}** ({classification}): "
                f"`{normalized.replace('`', 'BACKTICK')}`"
            )
        rendered.append("")

    header = [
        "# Exhaustive K source declaration and rule inventory",
        "",
        "Generated from the clean scratch copy. Each top-level source declaration, "
        "configuration/context, rule, claim, module/import, and syntax block is "
        "listed once in source order. Multiline declarations are normalized onto "
        "one line but retain their exact source span.",
        "",
        "## Counts",
        "",
        "| File | Syntax | Rules | Operational rules | Pure/equational rules | "
        "Simplification rules | Priority rules | Function syntax | Total syntax | "
        "Opaque/no-evaluators syntax | Claims |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for relative, counter in per_file.items():
        header.append(
            f"| `{relative}` | {counter['syntax']} | {counter['rule']} | "
            f"{counter['operational']} | {counter['pure/equational']} | "
            f"{counter['simplification']} | {counter['priority']} | "
            f"{counter['function']} | {counter['total']} | {counter['opaque']} | "
            f"{counter['claim']} |"
        )
    header.extend(
        [
            f"| **TOTAL** | {totals['syntax']} | {totals['rule']} | "
            f"{totals['operational']} | {totals['pure/equational']} | "
            f"{totals['simplification']} | {totals['priority']} | "
            f"{totals['function']} | {totals['total']} | {totals['opaque']} | "
            f"{totals['claim']} |",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(header + rendered) + "\n")
    print(f"files={len(SOURCE_FILES)}")
    print(f"syntax_declarations={totals['syntax']}")
    print(f"rules={totals['rule']}")
    print(f"operational_rules={totals['operational']}")
    print(f"pure_equational_rules={totals['pure/equational']}")
    print(f"simplification_rules={totals['simplification']}")
    print(f"priority_rules={totals['priority']}")
    print(f"function_syntax={totals['function']}")
    print(f"total_syntax={totals['total']}")
    print(f"opaque_syntax={totals['opaque']}")
    print(f"claims={totals['claim']}")
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()
