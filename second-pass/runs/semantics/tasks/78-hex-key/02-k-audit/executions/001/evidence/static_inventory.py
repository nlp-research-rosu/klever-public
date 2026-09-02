#!/usr/bin/env python3
"""Emit an exhaustive source-line inventory of K declarations and rules."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/78-hex-key")
OUTPUT = Path("/audit-output/evidence/static-rule-inventory.md")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
ENTRY_RE = re.compile(r"^\s*(syntax|configuration|context|rule|claim)\b")
ATTRIBUTE_WORDS = (
    "function",
    "total",
    "functional",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "trusted",
)

# Exact declaration/rule starts on the concrete and symbolic path of this
# submitted program. Strict/seqstrict-generated evaluation rules are represented
# by their syntax declaration starts.
USED_LINES: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {
        9, 32, 37, 41, 56, 57, 60, 61
    },
    "reference-semantics/semantics/core.k": {
        13, 15, 18, 25, 36, 37, 38, 39, 40, 42, 49, 124, 125, 126, 127,
        130, 131, 132, 157, 158, 185, 186, 189, 190, 191, 194, 199, 200,
        208, 209, 210, 213, 214, 215,
    },
    "reference-semantics/semantics/iter.k": {8},
    "reference-semantics/semantics/int.k": {9},
    "reference-semantics/semantics/str.k": {
        8, 9, 13, 14, 15, 16, 29, 32, 33, 34, 35, 37, 38, 39, 40
    },
    "reference-semantics/semantics/operators.k": {15, 16, 17},
    "reference-semantics/semantics/controls.k": {
        9, 20, 51, 52, 53, 54, 65, 69, 71, 72, 73, 85
    },
    "reference-semantics/semantics/functions.k": {
        8, 14, 63, 64, 78, 85
    },
    "reference-semantics/semantics/call.k": {19, 20, 21, 69},
    "reference-semantics/semantics/tuple.k": {31, 32},
    "verification.k": {8, 9, 14, 15, 22, 23, 28, 29, 32, 33, 34, 39, 40, 41},
    "spec.k": {9, 37},
}


def normalized(block: list[str]) -> str:
    text = " ".join(part.strip() for part in block)
    return re.sub(r"\s+", " ", text).replace("|", r"\|")


def attrs(block_text: str) -> str:
    found = [word for word in ATTRIBUTE_WORDS if re.search(rf"\b{re.escape(word)}\b", block_text)]
    priorities = re.findall(r"priority\((\d+)\)", block_text)
    found.extend(f"priority={value}" for value in priorities)
    return ", ".join(dict.fromkeys(found)) or "none"


def classification(path: Path, kind: str, block_text: str) -> str:
    supplied = "reference-semantics" in path.parts
    if supplied:
        if kind == "rule" and "<k>" in block_text:
            return "supplied operational semantics"
        if kind == "rule":
            return "supplied equation/helper"
        if kind == "syntax":
            return "supplied syntax/declaration"
        if kind == "context":
            return "supplied evaluation context"
        if kind == "configuration":
            return "supplied configuration"
        return "supplied baseline"
    if path.name == "verification.k":
        if kind == "syntax" and "macro" in block_text:
            return "candidate macro declaration"
        if kind == "rule" and ("hexKeyBody" in block_text or "hexKeyLoopBody" in block_text):
            return "candidate macro expansion"
        if kind == "syntax":
            return "candidate mathematical function declaration"
        if kind == "rule":
            return "candidate mathematical equation"
    if path.name == "spec.k" and kind == "claim":
        return "candidate positive reachability claim"
    return "other"


rows: list[tuple[str, int, str, str, str, str, str]] = []
counts: dict[tuple[str, str], int] = {}
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if ENTRY_RE.match(line)]
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        # Comments between declarations belong to neither declaration; trim them.
        raw_block = lines[start:stop]
        while raw_block and raw_block[-1].lstrip().startswith("//"):
            raw_block.pop()
        kind = ENTRY_RE.match(lines[start]).group(1)  # type: ignore[union-attr]
        block_text = normalized(raw_block)
        relative = path.relative_to(ROOT).as_posix()
        relevance = (
            "USED PATH"
            if start + 1 in USED_LINES.get(relative, set())
            else "not used by solution"
        )
        trust = (
            "trusted supplied semantics"
            if "reference-semantics" in path.parts
            else "candidate-local; reviewed"
        )
        rows.append(
            (
                relative,
                start + 1,
                kind,
                classification(path, kind, block_text),
                relevance,
                attrs(block_text),
                block_text,
            )
        )
        counts[(relative, kind)] = counts.get((relative, kind), 0) + 1

with OUTPUT.open("w", encoding="utf-8") as stream:
    stream.write("# Exhaustive K source inventory\n\n")
    stream.write(
        "Generated directly from the fresh scratch sources. Every source line beginning "
        "with `syntax`, `configuration`, `context`, `rule`, or `claim` is listed once. "
        "Supplied-semantics entries are the selected trusted semantics level; the USED "
        "PATH marker identifies entries whose text participates in the submitted "
        "program's execution or its proof helpers.\n\n"
    )
    stream.write("## Counts\n\n")
    stream.write("| File | syntax | configuration | context | rule | claim |\n")
    stream.write("|---|---:|---:|---:|---:|---:|\n")
    for path in FILES:
        relative = path.relative_to(ROOT).as_posix()
        stream.write(
            f"| `{relative}` | {counts.get((relative, 'syntax'), 0)} | "
            f"{counts.get((relative, 'configuration'), 0)} | "
            f"{counts.get((relative, 'context'), 0)} | "
            f"{counts.get((relative, 'rule'), 0)} | "
            f"{counts.get((relative, 'claim'), 0)} |\n"
        )
    stream.write(f"\nTotal inventoried entries: {len(rows)}.\n\n")
    stream.write("## Entries\n\n")
    stream.write("| Source | Kind | Classification | Relevance | Attributes | Source stanza |\n")
    stream.write("|---|---|---|---|---|---|\n")
    for relative, line, kind, cls, relevance, attributes, block in rows:
        stream.write(
            f"| `{relative}:{line}` | {kind} | {cls} | {relevance} | "
            f"{attributes} | `{block}` |\n"
        )

print(f"files={len(FILES)}")
print(f"entries={len(rows)}")
print(f"output={OUTPUT}")
for kind in ("syntax", "configuration", "context", "rule", "claim"):
    print(f"{kind}={sum(1 for row in rows if row[2] == kind)}")
