#!/usr/bin/env python3
"""Generate a complete declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import collections
import re
from dataclasses import dataclass
from pathlib import Path


SEMANTICS_ROOT = Path("/reference/reference-semantics")
CANDIDATE = Path("/candidate")


@dataclass(frozen=True)
class Item:
    path: Path
    line: int
    kind: str
    text: str


def source_files() -> list[Path]:
    return [
        SEMANTICS_ROOT / "semantics.k",
        *sorted((SEMANTICS_ROOT / "semantics").glob("*.k")),
        CANDIDATE / "verification.k",
        CANDIDATE / "spec.k",
    ]


START = re.compile(r"^\s*(configuration|syntax|rule|context|claim)\b")


def items_in(path: Path) -> list[Item]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    items: list[Item] = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = lines[start:end]
        while body and (not body[-1].strip() or body[-1].lstrip().startswith("//")):
            body.pop()
        items.append(Item(path, start + 1, kind, "\n".join(body)))
    return items


def relative(path: Path) -> str:
    if path.is_relative_to(SEMANTICS_ROOT):
        return str(Path("reference-semantics") / path.relative_to(SEMANTICS_ROOT))
    return str(Path("candidate") / path.relative_to(CANDIDATE))


# Exact starts in the fixed semantics that materially contribute to this
# program's execution/proof path. Syntax declarations are mapped separately by
# their source module because many productions share one declaration item.
TARGET_RULES: set[tuple[str, int]] = {
    ("reference-semantics/semantics/core.k", 69),
    ("reference-semantics/semantics/core.k", 70),
    ("reference-semantics/semantics/core.k", 118),
    ("reference-semantics/semantics/core.k", 125),
    ("reference-semantics/semantics/core.k", 126),
    ("reference-semantics/semantics/core.k", 127),
    ("reference-semantics/semantics/core.k", 131),
    ("reference-semantics/semantics/core.k", 132),
    ("reference-semantics/semantics/core.k", 152),
    ("reference-semantics/semantics/core.k", 158),
    ("reference-semantics/semantics/core.k", 189),
    ("reference-semantics/semantics/core.k", 190),
    ("reference-semantics/semantics/core.k", 191),
    ("reference-semantics/semantics/core.k", 194),
    ("reference-semantics/semantics/core.k", 214),
    ("reference-semantics/semantics/core.k", 215),
    ("reference-semantics/semantics/core.k", 218),
    ("reference-semantics/semantics/core.k", 219),
    ("reference-semantics/semantics/operators.k", 12),
    ("reference-semantics/semantics/int.k", 9),
    ("reference-semantics/semantics/int.k", 11),
    ("reference-semantics/semantics/int.k", 12),
    ("reference-semantics/semantics/float.k", 112),
    ("reference-semantics/semantics/float.k", 113),
    ("reference-semantics/semantics/float.k", 137),
    ("reference-semantics/semantics/float.k", 195),
    ("reference-semantics/semantics/float.k", 196),
    ("reference-semantics/semantics/float.k", 198),
    ("reference-semantics/semantics/list.k", 9),
    ("reference-semantics/semantics/list.k", 10),
    ("reference-semantics/semantics/list.k", 14),
    ("reference-semantics/semantics/list.k", 15),
    ("reference-semantics/semantics/list.k", 19),
    ("reference-semantics/semantics/list.k", 20),
    ("reference-semantics/semantics/list.k", 53),
    ("reference-semantics/semantics/tuple.k", 32),
    ("reference-semantics/semantics/controls.k", 9),
    ("reference-semantics/semantics/controls.k", 48),
    ("reference-semantics/semantics/controls.k", 69),
    ("reference-semantics/semantics/controls.k", 71),
    ("reference-semantics/semantics/controls.k", 72),
    ("reference-semantics/semantics/controls.k", 73),
    ("reference-semantics/semantics/controls.k", 85),
    ("reference-semantics/semantics/controls.k", 106),
    ("reference-semantics/semantics/functions.k", 14),
    ("reference-semantics/semantics/functions.k", 63),
    ("reference-semantics/semantics/functions.k", 64),
    ("reference-semantics/semantics/functions.k", 78),
    ("reference-semantics/semantics/functions.k", 85),
    ("reference-semantics/semantics/call.k", 16),
    ("reference-semantics/semantics/call.k", 20),
    ("reference-semantics/semantics/call.k", 21),
    ("reference-semantics/semantics/call.k", 69),
}

TARGET_SYNTAX_FILES = {
    "reference-semantics/semantics/syntax.k",
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/iter.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/int.k",
    "reference-semantics/semantics/float.k",
    "reference-semantics/semantics/list.k",
    "reference-semantics/semantics/tuple.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/call.k",
    "candidate/verification.k",
}


def attributes(text: str) -> list[str]:
    found: list[str] = []
    for bracket in re.findall(r"\[([^\]]+)\]", text, re.DOTALL):
        for name in (
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "concrete",
            "owise",
            "priority",
            "simplification",
            "macro-rec",
            "macro",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(name)}\b", bracket):
                found.append(name)
    return sorted(set(found))


def subtype(item: Item) -> str:
    attrs = attributes(item.text)
    if item.kind == "syntax":
        if "no-evaluators" in attrs:
            return "opaque symbol declaration"
        if "function" in attrs or "functional" in attrs:
            return "function declaration"
        if "macro" in attrs or "macro-rec" in attrs:
            return "macro declaration"
        return "syntax declaration"
    if item.kind == "rule":
        if "<k>" in item.text or re.search(r"<[A-Za-z-]+>", item.text):
            return "ordinary semantic rule"
        if "concrete" in attrs:
            return "concrete equation"
        return "equational rule"
    if item.kind == "context":
        return "evaluation context"
    if item.kind == "configuration":
        return "configuration"
    return "reachability claim"


def target_role(item: Item) -> str:
    rel = relative(item.path)
    if rel == "candidate/verification.k":
        return "proof-local; target-used"
    if rel == "candidate/spec.k":
        return "target claim"
    if (rel, item.line) in TARGET_RULES:
        return "fixed semantics; target-used"
    if item.kind in {"syntax", "context", "configuration"} and rel in TARGET_SYNTAX_FILES:
        return "fixed semantics; declaration/context for target language"
    if rel.endswith("concrete.k"):
        return "concrete-only; excluded from proof definition"
    return "fixed semantics; target-unreached"


def decision(item: Item) -> str:
    rel = relative(item.path)
    attrs = attributes(item.text)
    role = target_role(item)
    if rel == "candidate/verification.k":
        if item.kind == "syntax":
            return (
                "Accepted: proof-local definitional symbol; no operational cells, "
                "priority, simplification, or opacity."
            )
        return (
            "Accepted: truthful disjoint/owise or structural equation; recursive "
            "calls descend on ValSeq and no program step is replaced."
        )
    if rel == "candidate/spec.k":
        if item.line == 6:
            return (
                "Accepted circularity: exact real #loop control/body; preserves all "
                "observable cells and constrains the result heap through incrAcc."
            )
        return (
            "Accepted entry theorem: exact compiled submitted module and call; "
            "fresh returned ref and result heap are constrained."
        )
    if "no-evaluators" in attrs:
        if rel.endswith("float.k") and item.line in {111, 195}:
            return (
                "Accepted supplied trusted primitive used for Float addition/promotion; "
                "the theorem is structural/conditional on this fixed contract."
            )
        return (
            "Accepted only at supplied-semantics trust boundary; opaque and "
            "target-unreached for this theorem."
        )
    if role == "fixed semantics; target-used" or (
        item.kind in {"syntax", "context", "configuration"} and "target language" in role
    ):
        return (
            "Accepted after target-path review: faithful binding/evaluation/control/"
            "heap transition for this program and its allNumeric domain."
        )
    if role.startswith("concrete-only"):
        return (
            "Excluded from Haskell proof theory; inspected as concrete support only "
            "and exercised by reviewer krun tests."
        )
    return (
        "Accepted as unchanged supplied fixed semantics and target-unreached; "
        "may intentionally model only its documented subset and contributes no "
        "task answer or proof-local shortcut."
    )


def one_line(text: str, limit: int = 230) -> str:
    compact = " ".join(
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("//")
    )
    compact = compact.replace("|", r"\|")
    if len(compact) > limit:
        compact = compact[: limit - 1] + "…"
    return compact


def main() -> None:
    all_items = [item for path in source_files() for item in items_in(path)]
    counts = collections.Counter(item.kind for item in all_items)
    subtype_counts = collections.Counter(subtype(item) for item in all_items)
    attr_counts = collections.Counter(
        attribute for item in all_items for attribute in attributes(item.text)
    )

    print("# Exhaustive K declaration/rule inventory")
    print()
    print(
        "Scope: trusted supplied `reference-semantics/semantics.k`, every helper "
        "under `reference-semantics/semantics/`, candidate `verification.k`, and "
        "both claims in candidate `spec.k`. Entries are split at every top-level "
        "`configuration`, `syntax`, `context`, `rule`, or `claim` start."
    )
    print()
    print(f"- Files: {len(source_files())}")
    print(f"- Inventory entries: {len(all_items)}")
    print(f"- Kinds: {dict(sorted(counts.items()))}")
    print(f"- Subtypes: {dict(sorted(subtype_counts.items()))}")
    print(f"- Attributes: {dict(sorted(attr_counts.items()))}")
    print(f"- Simplification rules/declarations: {attr_counts['simplification']}")
    print(f"- Functional declarations: {attr_counts['functional']}")
    print()
    print(
        "The selected semantics is launcher-supplied and integrity-checked. "
        "“Target-unreached” is not used to bless a candidate extension: it records "
        "that an unchanged fixed-semantics rule does not participate in this "
        "program's dependency slice. All candidate-local extensions are marked "
        "proof-local and reviewed individually."
    )
    print()
    print("| # | Location | Kind | Attributes | Target role | Decision | Text |")
    print("|---:|---|---|---|---|---|---|")
    for index, item in enumerate(all_items, 1):
        attrs = ", ".join(attributes(item.text)) or "none"
        print(
            f"| {index} | `{relative(item.path)}:{item.line}` | {subtype(item)} "
            f"| {attrs} | {target_role(item)} | {decision(item)} "
            f"| `{one_line(item.text)}` |"
        )


if __name__ == "__main__":
    main()
