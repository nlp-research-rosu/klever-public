#!/usr/bin/env python3
"""Produce a line-addressed inventory of every K declaration and rule."""

from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/tmp/audit-work/0-has-close-elements")
SEMANTICS_ROOT = ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/rule-inventory.md")

START = re.compile(
    r'^\s*(?:(requires)\s+"|(module|imports|endmodule|syntax|configuration|rule|claim|context)\b)'
)
INTERESTING = {
    "requires",
    "module",
    "imports",
    "syntax",
    "configuration",
    "rule",
    "claim",
    "context",
}


def without_comments(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def normalize(text: str) -> str:
    return " ".join(without_comments(text).split())


def classify(kind: str, text: str) -> list[str]:
    clean = without_comments(text)
    tags = [kind]
    attributes = {
        "function": r"(?<![-\w])function(?![-\w])",
        "total": r"(?<![-\w])total(?![-\w])",
        "functional": r"(?<![-\w])functional(?![-\w])",
        "symbol": r"\bsymbol\s*\(",
        "no-evaluators": r"\bno-evaluators\b",
        "priority": r"\bpriority\s*\(",
        "simplification": r"\bsimplification\b",
        "concrete": r"\bconcrete\b",
        "owise": r"\bowise\b",
        "macro": r"\bmacro\b",
        "strict": r"(?<!seq)\bstrict(?:\s*\(|\b)",
        "seqstrict": r"\bseqstrict(?:\s*\(|\b)",
        "token": r"\btoken\b",
    }
    for tag, pattern in attributes.items():
        if re.search(pattern, clean):
            tags.append(tag)
    if "symbol" in tags and "no-evaluators" in tags:
        tags.append("opaque-symbol")
    if kind == "rule" and not any(
        tag in tags for tag in ("simplification", "concrete", "macro")
    ):
        tags.append("ordinary-rule")
    return tags


def inventory_file(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            kind = match.group(1) or match.group(2)
            starts.append((index, kind))
    records = []
    for position, (start, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        if kind not in INTERESTING:
            continue
        block = "\n".join(lines[start:stop]).rstrip()
        records.append(
            {
                "line": start + 1,
                "kind": kind,
                "tags": classify(kind, block),
                "normalized": normalize(block),
            }
        )
    return records


def main() -> int:
    paths = sorted(SEMANTICS_ROOT.rglob("*.k")) + [
        ROOT / "verification.k",
        ROOT / "spec.k",
    ]
    totals = Counter()
    by_file = defaultdict(Counter)
    all_records = {}
    hashes = {}
    for path in paths:
        data = path.read_bytes()
        hashes[path] = hashlib.sha256(data).hexdigest()
        records = inventory_file(path)
        all_records[path] = records
        for record in records:
            for tag in record["tags"]:
                totals[tag] += 1
                by_file[path][tag] += 1

    out = []
    out.append("# Exhaustive K source inventory")
    out.append("")
    out.append(
        "Generated from the clean scratch copy. Each entry is keyed by source "
        "file and starting line; multiline declarations/rules are normalized "
        "onto one line. `ordinary-rule` excludes only rules explicitly marked "
        "`simplification` or `concrete`."
    )
    out.append("")
    out.append("## Global counts")
    out.append("")
    for key, value in sorted(totals.items()):
        out.append(f"- `{key}`: {value}")
    out.append("")
    out.append("## Per-file counts and SHA-256")
    out.append("")
    out.append("| File | SHA-256 | Counts |")
    out.append("|---|---|---|")
    for path in paths:
        rel = path.relative_to(ROOT)
        counts = ", ".join(
            f"{key}={value}" for key, value in sorted(by_file[path].items())
        )
        out.append(f"| `{rel}` | `{hashes[path]}` | {counts} |")
    out.append("")
    out.append("## Line-addressed declarations and rules")
    for path in paths:
        rel = path.relative_to(ROOT)
        out.append("")
        out.append(f"### `{rel}`")
        out.append("")
        for record in all_records[path]:
            tags = ", ".join(record["tags"])
            statement = record["normalized"].replace("`", "\\`")
            out.append(
                f"- L{record['line']} [{tags}] `{statement}`"
            )

    OUTPUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"output={OUTPUT}")
    print(f"files={len(paths)}")
    print(f"records={sum(len(records) for records in all_records.values())}")
    print("global_counts=" + repr(dict(sorted(totals.items()))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
