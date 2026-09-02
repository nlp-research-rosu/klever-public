#!/usr/bin/env python3
"""Create a source-line-indexed inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/62-derivative")
OUT = Path("/audit-output/evidence/stage5_rule_inventory.md")
DECL_RE = re.compile(r"^\s{2}(configuration|syntax|context|rule|claim)\b")
ATTR_NAMES = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "macro",
    "strict",
    "seqstrict",
    "simplification",
    "concrete",
    "owise",
    "priority",
    "token",
    "bracket",
)


def normalized(block: list[str]) -> str:
    parts = []
    for line in block:
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        parts.append(stripped)
    return " ".join(parts)


def attributes(text: str) -> list[str]:
    found = []
    for name in ATTR_NAMES:
        if name == "priority":
            matches = re.findall(r"priority\([^)]*\)", text)
            found.extend(matches)
        elif re.search(rf"\b{re.escape(name)}\b", text):
            found.append(name)
    return found


def classify(kind: str, text: str) -> str:
    if kind == "rule":
        if "simplification" in text:
            return "rule-simplification"
        if "concrete" in text:
            return "rule-concrete"
        if "priority(" in text:
            return "rule-priority"
        if "owise" in text:
            return "rule-owise"
        return "rule-ordinary"
    return kind


def disposition(file_name: str, line: int, kind: str, text: str) -> str:
    if file_name.startswith("reference-semantics/"):
        if kind == "syntax" and (
            "no-evaluators" in text or "symbol(" in text or "functional" in text
        ):
            return (
                "ACCEPTED SUPPLIED TRUST BOUNDARY: byte-pinned baseline "
                "declaration; not reached by this integer-only program proof."
            )
        return (
            "ACCEPTED AT SELECTED SEMANTICS LEVEL: byte-pinned supplied "
            "baseline; candidate did not add or alter it. Used-path fidelity "
            "is mapped separately."
        )
    if file_name == "spec.k":
        return (
            "PROOF OBLIGATION, NOT AN ASSUMED RULE: reconstructed dynamically "
            "and reviewed for adequacy."
        )
    if file_name != "verification.k":
        return "REVIEWED; see source-specific discussion."

    if line == 9:
        return "ACCEPT: free inductive syntax for finite integer sequences."
    if line in (11, 12, 13):
        return "ACCEPT: total structural embedding of IntVals into ValSeq."
    if line in (18, 20, 22, 24, 26):
        return (
            "ACCEPT ON ALL REACHABLE USES: truthful derivative fold; the "
            "non-total N<0 case is unreachable because entry starts at 0 and "
            "the loop claim requires N>0."
        )
    if line == 39:
        return (
            "REJECT AS GLOBAL REPRESENTATION EXTENSION: adds a noncanonical "
            "ValSeq constructor and makes inherited total ValSeq helpers "
            "non-exhaustive."
        )
    if line == 40:
        return (
            "UNSOUND — REJECT: proves every symbolic enumerated list nonempty, "
            "but VS=.IntVals is empty; see stage5_symbolic_false_witness.log "
            "and stage5_ground_contradiction.log."
        )
    if line in (44, 46):
        return (
            "LOCALLY CORRECT ITERATOR STEP for the proposed lazy constructor "
            "and continuation-preserving, but depends on the rejected global "
            "representation bridge."
        )
    if line in (53, 54):
        return "ACCEPT: macro is byte-for-structure equal to the real loop target."
    if line in (57, 58):
        return "ACCEPT: macro is byte-for-structure equal to the real loop body."
    if line in (72, 73):
        return "ACCEPT: macro is byte-for-structure equal to the translated function body."
    return "REVIEWED PROOF-LOCAL ITEM; see Stage 5 narrative."


def main() -> int:
    sources = [ROOT / "reference-semantics" / "semantics.k"]
    sources.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
    sources.extend([ROOT / "verification.k", ROOT / "spec.k"])

    entries = []
    for path in sources:
        lines = path.read_text(encoding="utf-8").splitlines()
        starts = [i for i, line in enumerate(lines) if DECL_RE.match(line)]
        for ordinal, start in enumerate(starts):
            end = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
            match = DECL_RE.match(lines[start])
            assert match is not None
            kind = match.group(1)
            block = lines[start:end]
            text = normalized(block)
            # Strip trailing module delimiters accidentally captured by the last block.
            text = re.sub(r"\s+(?:end)?module\b.*$", "", text)
            rel = path.relative_to(ROOT)
            entries.append(
                {
                    "file": str(rel),
                    "line": start + 1,
                    "kind": classify(kind, text),
                    "attrs": attributes(text),
                    "text": text,
                    "disposition": disposition(
                        str(rel), start + 1, classify(kind, text), text
                    ),
                }
            )

    by_file: dict[str, collections.Counter[str]] = collections.defaultdict(
        collections.Counter
    )
    totals: collections.Counter[str] = collections.Counter()
    for entry in entries:
        by_file[entry["file"]][entry["kind"]] += 1
        totals[entry["kind"]] += 1

    out = []
    out.append("# Exhaustive K declaration and rule inventory")
    out.append("")
    out.append(
        "Sources: the fresh scratch copy of the byte-verified supplied semantics, "
        "candidate `verification.k`, and candidate `spec.k`. Every declaration "
        "beginning with `configuration`, `syntax`, `context`, `rule`, or `claim` "
        "is listed once with its source line."
    )
    out.append("")
    out.append("## Counts by file")
    out.append("")
    out.append("| File | Counts |")
    out.append("|---|---|")
    for file_name in sorted(by_file):
        rendered = ", ".join(
            f"{kind}={count}" for kind, count in sorted(by_file[file_name].items())
        )
        out.append(f"| `{file_name}` | {rendered} |")
    out.append("")
    out.append(
        "**Totals:** "
        + ", ".join(f"{kind}={count}" for kind, count in sorted(totals.items()))
    )

    out.append("")
    out.append("## Complete line-indexed inventory")
    out.append("")
    out.append(
        "| # | Source | Kind | Attributes | Normalized declaration/rule | "
        "Audit disposition |"
    )
    out.append("|---:|---|---|---|---|---|")
    for index, entry in enumerate(entries, 1):
        text = entry["text"].replace("|", "&#124;").replace("`", "&#96;")
        attrs = ", ".join(entry["attrs"]) or "—"
        out.append(
            f"| {index} | `{entry['file']}:{entry['line']}` | "
            f"{entry['kind']} | {attrs} | {text} | {entry['disposition']} |"
        )

    selected_groups = {
        "Simplification rules": lambda e: e["kind"] == "rule-simplification",
        "Priority rules": lambda e: e["kind"] == "rule-priority",
        "Concrete-only rules": lambda e: e["kind"] == "rule-concrete",
        "Opaque/symbol/no-evaluators declarations": lambda e: (
            e["kind"] == "syntax"
            and any(
                attr in e["attrs"]
                for attr in ("symbol", "no-evaluators", "functional")
            )
        ),
        "Total declarations": lambda e: (
            e["kind"] == "syntax" and "total" in e["attrs"]
        ),
    }
    for heading, predicate in selected_groups.items():
        out.append("")
        out.append(f"## {heading}")
        out.append("")
        selected = [entry for entry in entries if predicate(entry)]
        if not selected:
            out.append("None.")
            continue
        for entry in selected:
            attrs = ", ".join(entry["attrs"]) or "—"
            out.append(
                f"- `{entry['file']}:{entry['line']}` ({attrs}): "
                f"{entry['text']}"
            )

    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"INVENTORY_PATH: {OUT}")
    print(f"INVENTORY_ENTRIES: {len(entries)}")
    print(
        "TOTALS: "
        + ", ".join(f"{kind}={count}" for kind, count in sorted(totals.items()))
    )
    print(f"INVENTORY_BYTES: {OUT.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
