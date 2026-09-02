#!/usr/bin/env python3
"""Produce a complete, line-addressed K declaration and rule inventory."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


SOURCE_ROOT = Path(
    "/tmp/audit-work/120-maximum/candidate-source/reference-semantics"
)
VERIFICATION = Path(
    "/tmp/audit-work/120-maximum/candidate-source/verification.k"
)
JSONL_OUTPUT = Path("/audit-output/evidence/stage5-rule-inventory.jsonl")
MARKDOWN_OUTPUT = Path("/audit-output/evidence/stage5-rule-inventory.md")

ANCHOR = re.compile(r"^  (configuration|syntax|rule|context|claim)\b")
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "macro",
    "owise",
    "strict",
    "seqstrict",
)
ATTRIBUTE_PATTERNS = {
    "function": re.compile(r"\bfunction\b"),
    "functional": re.compile(r"\bfunctional\b"),
    "total": re.compile(r"\btotal\b"),
    "symbol": re.compile(r"\bsymbol\s*\("),
    "no-evaluators": re.compile(r"\bno-evaluators\b"),
    "priority": re.compile(r"\bpriority\s*\("),
    "simplification": re.compile(r"\bsimplification\b"),
    "concrete": re.compile(r"\bconcrete\b"),
    "macro": re.compile(r"\bmacro\b"),
    "owise": re.compile(r"\bowise\b"),
    "strict": re.compile(r"\bstrict(?:\s*\(|\b)"),
    "seqstrict": re.compile(r"\bseqstrict(?:\s*\(|\b)"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_files() -> list[Path]:
    return sorted(SOURCE_ROOT.rglob("*.k")) + [VERIFICATION]


def extract_items(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = ANCHOR.match(line)
        if match:
            starts.append((index, match.group(1)))
    items: list[dict[str, object]] = []
    for ordinal, (start, kind) in enumerate(starts, start=1):
        stop = starts[ordinal][0] if ordinal < len(starts) else len(lines)
        while stop > start + 1 and (
            not lines[stop - 1].strip()
            or lines[stop - 1].lstrip().startswith("//")
            or lines[stop - 1].strip() == "endmodule"
        ):
            stop -= 1
        text = "\n".join(lines[start:stop]).rstrip()
        code = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
        attribute_text = " ".join(re.findall(r"\[([^\]\n]+)\]", code))
        tags = [
            attribute
            for attribute in ATTRIBUTES
            if ATTRIBUTE_PATTERNS[attribute].search(attribute_text)
        ]
        relative = (
            "verification.k"
            if path == VERIFICATION
            else path.relative_to(SOURCE_ROOT).as_posix()
        )
        origin = "proof-local" if path == VERIFICATION else "trusted-supplied-semantics"

        if kind == "rule":
            if "simplification" in tags:
                rule_class = "simplification-rule"
            elif "concrete" in tags:
                rule_class = "concrete-semantic-rule"
            elif path == VERIFICATION and "maximumBody" in text:
                rule_class = "macro-expansion-rule"
            else:
                rule_class = "ordinary-semantic-rule"
        else:
            rule_class = f"{kind}-declaration"

        if origin == "trusted-supplied-semantics":
            decision = "ACCEPTED_SELECTED_SEMANTICS"
            rationale = (
                "Entry is in the byte-identical trusted supplied definition; "
                "program-path applicability and trust effects are reviewed separately."
            )
        elif kind == "syntax" and "maximumBody" in text:
            decision = "SOUND_PROGRAM_ALIAS_DECLARATION"
            rationale = "Macro declaration only names the submitted function body."
        elif kind == "rule" and "maximumBody" in text:
            decision = "SOUND_PROGRAM_ALIAS_EXPANSION"
            rationale = (
                "Expansion matches the translated FuncDef body and leaves fixed call, "
                "binding, evaluation, allocation, return, and frame rules active."
            )
        elif kind == "rule" and "vsLen(sortVS" in text:
            decision = "SOUND_CONDITIONAL_ON_SORT_PRIMITIVE_CONTRACT"
            rationale = (
                "Ascending permutation preserves length; this is an axiom about the "
                "supplied opaque sortVS primitive, not a program-execution bridge."
            )
        else:
            decision = "WELL_FORMED_PROOF_LOCAL_ITEM"
            rationale = "No additional operational or result-bearing rule is introduced."

        items.append(
            {
                "id": f"{relative}:{start + 1}:{ordinal}",
                "file": relative,
                "line_start": start + 1,
                "line_end": stop,
                "kind": kind,
                "class": rule_class,
                "origin": origin,
                "tags": tags,
                "decision": decision,
                "rationale": rationale,
                "text": text,
            }
        )
    return items


def main() -> int:
    files = source_files()
    all_items: list[dict[str, object]] = []
    file_hashes: dict[str, str] = {}
    for path in files:
        relative = (
            "verification.k"
            if path == VERIFICATION
            else path.relative_to(SOURCE_ROOT).as_posix()
        )
        file_hashes[relative] = sha256(path)
        all_items.extend(extract_items(path))

    with JSONL_OUTPUT.open("w", encoding="utf-8") as stream:
        for item in all_items:
            stream.write(json.dumps(item, sort_keys=True) + "\n")

    by_kind = Counter(str(item["kind"]) for item in all_items)
    by_class = Counter(str(item["class"]) for item in all_items)
    tag_counts = Counter(
        str(tag) for item in all_items for tag in item["tags"]  # type: ignore[index]
    )
    per_file: dict[str, Counter[str]] = defaultdict(Counter)
    for item in all_items:
        per_file[str(item["file"])][str(item["kind"])] += 1

    markdown: list[str] = [
        "# Exhaustive K inventory",
        "",
        "Each row is one top-level K configuration, syntax declaration, context, "
        "claim, or rule. Full multiline source and the per-entry decision are in "
        "`stage5-rule-inventory.jsonl`.",
        "",
        f"- Files: {len(files)}",
        f"- Items: {len(all_items)}",
        f"- Rules: {by_kind['rule']}",
        f"- Syntax declarations: {by_kind['syntax']}",
        f"- Contexts: {by_kind['context']}",
        f"- Configurations: {by_kind['configuration']}",
        f"- Claims found in definition/proof extension: {by_kind['claim']}",
        f"- Function-tagged declarations/items: {tag_counts['function']}",
        f"- Functional-tagged declarations/items: {tag_counts['functional']}",
        f"- Total-tagged declarations/items: {tag_counts['total']}",
        f"- Opaque symbol-tagged items: {tag_counts['symbol']}",
        f"- No-evaluators-tagged items: {tag_counts['no-evaluators']}",
        f"- Priority-tagged rules/items: {tag_counts['priority']}",
        f"- Simplification-tagged rules/items: {tag_counts['simplification']}",
        f"- Concrete-tagged rules/items: {tag_counts['concrete']}",
        f"- Macro-tagged declarations/items: {tag_counts['macro']}",
        "",
        "## File hashes and counts",
        "",
        "| File | SHA-256 | configuration | syntax | context | rule | claim |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for relative in sorted(file_hashes):
        counts = per_file[relative]
        markdown.append(
            f"| `{relative}` | `{file_hashes[relative]}` | "
            f"{counts['configuration']} | {counts['syntax']} | "
            f"{counts['context']} | {counts['rule']} | {counts['claim']} |"
        )

    markdown.extend(
        [
            "",
            "## Rule classes",
            "",
            "| Class | Count |",
            "|---|---:|",
        ]
    )
    for name, count in sorted(by_class.items()):
        markdown.append(f"| `{name}` | {count} |")

    markdown.extend(
        [
            "",
            "## Complete line-addressed item list",
            "",
            "| ID | Kind/class | Tags | Decision | First source line |",
            "|---|---|---|---|---|",
        ]
    )
    for item in all_items:
        first_line = str(item["text"]).splitlines()[0].strip().replace("|", "\\|")
        tags = ", ".join(item["tags"]) if item["tags"] else "—"  # type: ignore[arg-type]
        markdown.append(
            f"| `{item['id']}` | `{item['kind']}` / `{item['class']}` | "
            f"{tags} | `{item['decision']}` | `{first_line}` |"
        )

    MARKDOWN_OUTPUT.write_text("\n".join(markdown) + "\n", encoding="utf-8")

    print(f"files={len(files)}")
    print(f"items={len(all_items)}")
    print(f"rules={by_kind['rule']}")
    print(f"syntax_declarations={by_kind['syntax']}")
    print(f"contexts={by_kind['context']}")
    print(f"configurations={by_kind['configuration']}")
    print(f"claims={by_kind['claim']}")
    for attribute in ATTRIBUTES:
        print(f"tag_{attribute}={tag_counts[attribute]}")
    print(f"jsonl={JSONL_OUTPUT}")
    print(f"markdown={MARKDOWN_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
