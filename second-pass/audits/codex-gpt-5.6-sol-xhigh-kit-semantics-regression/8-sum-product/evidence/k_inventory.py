#!/usr/bin/env python3
"""Generate a line-numbered inventory of all K declarations and rules."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

SOURCE = Path("/tmp/audit-work/src")
SEMANTICS_ROOT = SOURCE / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/K-INVENTORY.md")

START = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim)\b"
)
BOUNDARY = re.compile(
    r"^\s*(?:syntax|rule|context|configuration|claim|module|endmodule)\b"
)
ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
    "token",
    "bracket",
)
RELEVANT_MODULE_FILES = {
    "syntax.k",
    "core.k",
    "iter.k",
    "list.k",
    "tuple.k",
    "int.k",
    "operators.k",
    "controls.k",
    "functions.k",
    "call.k",
}


def source_files() -> list[Path]:
    paths = [SEMANTICS_ROOT / "semantics.k"]
    paths.extend(sorted((SEMANTICS_ROOT / "semantics").glob("*.k")))
    paths.extend([SOURCE / "verification.k", SOURCE / "spec.k"])
    return paths


def blocks(path: Path) -> list[tuple[str, int, str]]:
    lines = path.read_text().splitlines()
    found: list[tuple[str, int, str]] = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        begin = index
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            index += 1
        text = "\n".join(lines[begin:index]).rstrip()
        found.append((kind, begin + 1, text))
    return found


def disposition(path: Path, kind: str) -> str:
    if path.name == "verification.k":
        return "PROOF_LOCAL_INDIVIDUAL_REVIEW"
    if path.name == "spec.k":
        return "TARGET_CLAIM_ADEQUACY_REVIEW"
    if path.parent.name == "semantics" and path.name in RELEVANT_MODULE_FILES:
        return "SUPPLIED_BASELINE_USED_PATH_REVIEW"
    return "SUPPLIED_BASELINE_UNUSED_PATH_REVIEW"


def main() -> None:
    files = source_files()
    counts: Counter[str] = Counter()
    per_file: dict[str, Counter[str]] = defaultdict(Counter)
    attribute_counts: Counter[str] = Counter()
    rendered: list[str] = []

    for path in files:
        rel = path.relative_to(SOURCE).as_posix()
        file_blocks = blocks(path)
        rendered.append(f"\n## `{rel}`\n")
        if not file_blocks:
            rendered.append("No local syntax/rule/context/configuration/claim declarations.\n")
            continue
        for serial, (kind, line, text) in enumerate(file_blocks, 1):
            counts[kind] += 1
            per_file[rel][kind] += 1
            uncommented = "\n".join(
                source_line.split("//", 1)[0] for source_line in text.splitlines()
            )
            attribute_text = " ".join(re.findall(r"\[[^\]]*\]", uncommented))
            attrs = [
                attribute
                for attribute in ATTRIBUTES
                if re.search(rf"(?<![\w-]){re.escape(attribute)}(?![\w-])", attribute_text)
            ]
            for attribute in attrs:
                attribute_counts[attribute] += 1
            flat = " ".join(part.strip() for part in text.splitlines() if part.strip())
            rendered.append(
                f"- `{rel}:{line}` `{kind.upper()}-{serial:03d}` "
                f"disposition=`{disposition(path, kind)}` "
                f"attributes=`{','.join(attrs) if attrs else 'none'}`\n\n"
                f"  ```k\n{text}\n  ```\n"
            )

    header = [
        "# Exhaustive K declaration and rule inventory",
        "",
        "Generated from the clean scratch source copy. Each entry records the complete",
        "local declaration/rule block, source line, detected attributes, and review bucket.",
        "The supplied baseline bucket is not used to bless `verification.k`; its ten",
        "proof-local rules are inventoried separately as proof-local extensions.",
        "",
        "## Totals",
        "",
        f"- Files: {len(files)}",
        f"- Syntax declarations: {counts['syntax']}",
        f"- Ordinary rules: {counts['rule']}",
        f"- Context declarations: {counts['context']}",
        f"- Configurations: {counts['configuration']}",
        f"- Claims: {counts['claim']}",
        "- Detected attributes: "
        + str({attribute: attribute_counts[attribute] for attribute in ATTRIBUTES}),
        "",
        "## Per-file counts",
        "",
        "| File | Syntax | Rules | Contexts | Configurations | Claims |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for path in files:
        rel = path.relative_to(SOURCE).as_posix()
        item = per_file[rel]
        header.append(
            f"| `{rel}` | {item['syntax']} | {item['rule']} | "
            f"{item['context']} | {item['configuration']} | {item['claim']} |"
        )

    OUTPUT.write_text("\n".join(header + rendered) + "\n")
    print(f"inventory={OUTPUT}")
    print(f"files={len(files)}")
    print(f"counts={dict(counts)}")
    print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")

    raw_rules = sum(
        1
        for path in files
        for line in path.read_text().splitlines()
        if re.match(r"^\s*rule\b", line)
    )
    raw_syntax = sum(
        1
        for path in files
        for line in path.read_text().splitlines()
        if re.match(r"^\s*syntax\b", line)
    )
    print(f"raw_rule_starts={raw_rules}")
    print(f"raw_syntax_starts={raw_syntax}")
    if raw_rules != counts["rule"] or raw_syntax != counts["syntax"]:
        raise SystemExit("inventory start-count mismatch")
    print("INVENTORY_CROSSCHECK=PASS")


if __name__ == "__main__":
    main()
