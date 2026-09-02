#!/usr/bin/env python3
"""Exhaustive source-level inventory of K declarations, rules, and claims."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/reference/reference-semantics")
FILES = [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k"))]
FILES += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

START = re.compile(r"^\s*(syntax|rule|configuration|context|claim)\b")
ATTRS = (
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "concrete",
    "symbol",
    "no-evaluators",
    "owise",
    "anywhere",
    "macro",
    "strict",
    "seqstrict",
)

# Source ranges on the actual max_element path. Everything else in the supplied
# definition is still inventoried, but is not reachable from this program/claim.
USED_RANGES: dict[str, tuple[tuple[int, int], ...]] = {
    "semantics/syntax.k": ((9, 13), (28, 30), (50, 61)),
    "semantics/core.k": (
        (13, 60),
        (124, 191),
        (213, 219),
    ),
    "semantics/list.k": ((8, 10),),
    "semantics/functions.k": ((8, 20), (62, 90)),
    "semantics/builtins.k": ((75, 84),),
    "semantics/call.k": ((18, 32), (69, 75)),
}


def relative(path: Path) -> str:
    if path.is_relative_to(ROOT):
        return str(path.relative_to(ROOT))
    return "candidate/" + path.name


def is_used(rel: str, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in USED_RANGES.get(rel, ()))


entries: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:stop]
        # Trim comments/blank lines that introduce the next conceptual section.
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()
        match = START.match(lines[start])
        assert match is not None
        kind = match.group(1)
        block = "\n".join(block_lines)
        attrs = [attr for attr in ATTRS if re.search(rf"\b{re.escape(attr)}\b", block)]
        rel = relative(path)
        used = rel.startswith("candidate/") or is_used(rel, start + 1)
        if kind == "syntax":
            classification = "syntax-declaration"
        elif kind == "configuration":
            classification = "configuration"
        elif kind == "claim":
            classification = "reachability-claim"
        elif "<k>" in block or re.search(r"<[A-Za-z][^>]*>", block):
            classification = "operational-rule"
        else:
            classification = "equational-rule"

        if rel == "candidate/verification.k":
            if start + 1 in (9,):
                review = "ACCEPTED_EXACT_PROGRAM_CONSTANT"
            elif start + 1 in (19, 20):
                review = "ACCEPTED_MATHEMATICAL_FOLD_EQUATION"
            elif start + 1 in (25, 28):
                review = "LOCALLY_SOUND_ABSTRACT_ITERATOR; REAL-VALSEQ_CONNECTION_GAP"
            else:
                review = "ACCEPTED_LOCAL_DECLARATION"
        elif rel == "candidate/spec.k":
            review = "CLAIM_AUDITED_SEPARATELY"
        elif used:
            review = "ACCEPTED_SUPPLIED_FIXED_USED_PATH"
        elif "no-evaluators" in attrs:
            review = "SUPPLIED_OPAQUE_UNUSED_BY_TARGET"
        else:
            review = "ACCEPTED_SUPPLIED_FIXED_UNREACHED_BY_TARGET"

        head = " ".join(part.strip() for part in block_lines if part.strip())
        if len(head) > 360:
            head = head[:357] + "..."
        entries.append(
            {
                "file": rel,
                "line": start + 1,
                "kind": kind,
                "classification": classification,
                "attrs": ",".join(attrs) or "-",
                "used": "yes" if used else "no",
                "review": review,
                "head": head,
            }
        )

print("# Exhaustive K source inventory")
print()
print(
    "Generated directly from every `syntax`, `rule`, `configuration`, `context`, "
    "and `claim` declaration in the trusted supplied semantics tree and the "
    "candidate's verification/spec files."
)
print()
print(f"TOTAL_ENTRIES={len(entries)}")
for key in ("syntax", "rule", "configuration", "context", "claim"):
    print(f"{key.upper()}_COUNT={sum(1 for entry in entries if entry['kind'] == key)}")
print(
    "SIMPLIFICATION_COUNT="
    + str(sum(1 for entry in entries if "simplification" in str(entry["attrs"])))
)
print(
    "OPAQUE_NO_EVALUATORS_COUNT="
    + str(sum(1 for entry in entries if "no-evaluators" in str(entry["attrs"])))
)
print()
print("| # | file:line | kind/class | attrs | target path | review | source head |")
print("|---:|---|---|---|---|---|---|")
for index, entry in enumerate(entries, 1):
    head = str(entry["head"]).replace("|", "\\|").replace("`", "'")
    print(
        f"| {index} | `{entry['file']}:{entry['line']}` | "
        f"{entry['kind']} / {entry['classification']} | `{entry['attrs']}` | "
        f"{entry['used']} | {entry['review']} | {head} |"
    )
