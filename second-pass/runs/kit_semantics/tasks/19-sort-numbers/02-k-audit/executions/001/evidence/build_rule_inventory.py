#!/usr/bin/env python3
"""Build a complete line-addressed K declaration/rule/claim inventory."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/19-sort-numbers")
SEMANTICS = ROOT / "reference-semantics"
OUTPUT_JSON = Path("/audit-output/evidence/05-rule-inventory.json")
OUTPUT_MD = Path("/audit-output/evidence/05-rule-inventory.md")
START = re.compile(r"^\s*(syntax|configuration|rule|claim|context|alias)\b")
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "macro",
    "symbol",
    "no-evaluators",
    "concrete",
    "simplification",
    "priority",
    "owise",
    "anywhere",
)
USED_MODULES = {
    "semantics/syntax.k",
    "semantics/core.k",
    "semantics/str.k",
    "semantics/tuple.k",
    "semantics/methods.k",
    "semantics/functions.k",
    "semantics/builtins.k",
    "semantics/call.k",
    "semantics/sort.k",
}


def source_files() -> list[Path]:
    files = [SEMANTICS / "semantics.k"]
    files.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
    files.extend([ROOT / "verification.k", ROOT / "spec.k"])
    return files


def disposition(relative: str, kind: str, text: str) -> tuple[str, str]:
    compact = " ".join(text.split())
    if relative == "verification.k":
        if kind == "syntax":
            if "expectedSortNumbers" in compact:
                return "trust-dependent definition", "result summary depends on supplied opaque sortKeyVS"
            if "numberKeyClosure" in compact or "sortNumbersClosure" in compact:
                return "declaration", "candidate macro declaration; closure term is checked mechanically"
            if "isNumberWord" in compact or "allNumberWords" in compact:
                return "definition", "candidate decidable input-predicate declaration"
        if kind == "rule":
            if "expectedSortNumbers" in compact:
                return "definitional summary", "truthful execution summary conditional on supplied sortKeyVS contract"
            if "numberKeyClosure" in compact or "sortNumbersClosure" in compact:
                return "macro expansion", "exact translated constructor body; no execution bypass"
            if "isNumberWord" in compact or "allNumberWords" in compact:
                return "definitional equation", "truthful finite/structural predicate equation"
        return "candidate extension", "reviewed individually in REVIEW.md"
    if relative == "spec.k":
        return "reachability claim", "positive theorem target; reconstructed independently"
    if "sortKeyVS" in compact:
        if kind == "syntax":
            return "trusted opaque primitive", "result-bearing supplied symbol with no proof-backend equations"
        return "trusted primitive dispatch", "supplied sorted(key=...) operational rule returns opaque sortKeyVS"
    if "semantics/concrete.k" in relative:
        return "concrete-only semantic rule", "LLVM validation leg; absent from proof module MPY"
    if relative.startswith("reference-semantics/"):
        short = relative.removeprefix("reference-semantics/")
        if short in USED_MODULES:
            return "fixed relevant semantics", "used directly or transitively by the submitted program"
        return "fixed unused/general semantics", "not exercised by this program; no candidate modification"
    return "assembly declaration", "fixed supplied module assembly"


def main() -> int:
    entries = []
    for path in source_files():
        relative = path.relative_to(ROOT).as_posix()
        lines = path.read_text().splitlines()
        starts = [
            (index, START.match(line).group(1))
            for index, line in enumerate(lines)
            if START.match(line)
        ]
        for position, (start, kind) in enumerate(starts):
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            block_lines = lines[start:end]
            while block_lines and not block_lines[-1].strip():
                block_lines.pop()
            text = "\n".join(block_lines)
            attributes = [attribute for attribute in ATTRIBUTES if attribute in text]
            category, decision = disposition(relative, kind, text)
            entries.append(
                {
                    "id": len(entries) + 1,
                    "file": relative,
                    "line": start + 1,
                    "kind": kind,
                    "attributes": attributes,
                    "category": category,
                    "decision": decision,
                    "text": text,
                }
            )

    OUTPUT_JSON.write_text(json.dumps(entries, indent=2) + "\n")
    markdown = [
        "# Exhaustive K declaration, rule, and claim inventory",
        "",
        f"Entries: {len(entries)}. Each entry is line-addressed and includes its complete block through the next declaration/rule/claim.",
        "",
        "| ID | Location | Kind | Attributes | Category | Audit decision |",
        "|---:|---|---|---|---|---|",
    ]
    for entry in entries:
        attrs = ", ".join(entry["attributes"]) or "none"
        markdown.append(
            f"| {entry['id']} | `{entry['file']}:{entry['line']}` | "
            f"{entry['kind']} | {attrs} | {entry['category']} | {entry['decision']} |"
        )
    markdown.extend(
        [
            "",
            "The companion JSON contains the full source text for every row; the table does not truncate rule bodies.",
            "",
        ]
    )
    OUTPUT_MD.write_text("\n".join(markdown))
    print(f"inventory_entries={len(entries)}")
    for kind in sorted({entry["kind"] for entry in entries}):
        print(f"{kind}_count={sum(entry['kind'] == kind for entry in entries)}")
    for category in sorted({entry["category"] for entry in entries}):
        print(
            f"category_count {category}="
            f"{sum(entry['category'] == category for entry in entries)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
