#!/usr/bin/env python3
"""Build a line-addressable inventory of every K declaration in audit scope."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/69-search")
semantic_files = sorted((SCRATCH / "reference-semantics").rglob("*.k"))
files = semantic_files + [SCRATCH / "verification.k", SCRATCH / "spec.k"]
starter = re.compile(r"^\s*(syntax|rule|claim|context|configuration)\b")
stopper = re.compile(r"^\s*(module|endmodule|imports)\b")
flags_to_find = [
    "function",
    "functional",
    "total",
    "macro",
    "simplification",
    "concrete",
    "owise",
    "priority",
    "strict",
    "seqstrict",
    "symbol",
    "hook",
    "token",
]


def relative(path: Path) -> str:
    return str(path.relative_to(SCRATCH))


entries: list[dict[str, object]] = []
for path in files:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if starter.match(line)]
    for number, start in enumerate(starts):
        upper = starts[number + 1] if number + 1 < len(starts) else len(lines)
        end = upper
        for index in range(start + 1, upper):
            if stopper.match(lines[index]):
                end = index
                break
        while end > start + 1 and (
            not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        block_lines = [
            line.strip()
            for line in lines[start:end]
            if line.strip() and not line.lstrip().startswith("//")
        ]
        block = " ".join(block_lines)
        kind = starter.match(lines[start]).group(1)  # type: ignore[union-attr]
        found_flags = [flag for flag in flags_to_find if re.search(rf"\b{re.escape(flag)}\b", block)]
        if path.name == "verification.k":
            disposition = "PROOF-LOCAL—individual decision in REVIEW.md"
        elif path.name == "spec.k":
            disposition = "ENTRY CLAIM—adequacy decision in REVIEW.md"
        else:
            disposition = "TRUSTED-SUPPLIED baseline (byte-identical)"
        entries.append({
            "path": relative(path),
            "start": start + 1,
            "end": end,
            "kind": kind,
            "flags": ",".join(found_flags) or "—",
            "head": block[:240],
            "disposition": disposition,
        })

counts = Counter(entry["kind"] for entry in entries)
print("# Exhaustive K declaration and rule inventory")
print()
print("Scope: all `.k` files in the byte-identical supplied semantics tree, "
      "plus candidate `verification.k` and `spec.k`. Each entry identifies the "
      "complete source block by inclusive line range; `head` is only a compact preview.")
print()
print(f"Files: {len(files)}; declarations: {len(entries)}; "
      + "; ".join(f"{kind}={count}" for kind, count in sorted(counts.items())))
print()
print("| # | source lines | kind | detected attributes | compact head | audit disposition |")
print("|---:|---|---|---|---|---|")
for index, entry in enumerate(entries, 1):
    head = str(entry["head"]).replace("|", "\\|").replace("`", "'")
    print(
        f"| {index} | `{entry['path']}:{entry['start']}-{entry['end']}` "
        f"| {entry['kind']} | {entry['flags']} | `{head}` | {entry['disposition']} |"
    )

print()
print("## Attribute searches")
print()
for flag in flags_to_find:
    matching = [entry for entry in entries if flag in str(entry["flags"]).split(",")]
    print(f"- `{flag}`: {len(matching)} declaration block(s)")
    for entry in matching:
        print(f"  - `{entry['path']}:{entry['start']}-{entry['end']}`")
