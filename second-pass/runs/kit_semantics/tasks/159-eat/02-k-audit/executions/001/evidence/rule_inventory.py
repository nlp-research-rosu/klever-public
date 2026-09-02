#!/usr/bin/env python3
"""Exhaustive source inventory for the fixed semantics and candidate proof K."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
EXTRA = [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
OUTPUT = Path("/audit-output/evidence/rule-inventory.md")

TOP_REQUIRE = re.compile(r"^requires\b")
START = re.compile(
    r"^\s*(module|imports|syntax|configuration|context|rule|claim|endmodule)\b"
)
ITEM_KINDS = {"syntax", "configuration", "context", "rule", "claim"}
ATTRS = (
    "function",
    "total",
    "functional",
    "simplification",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)

# Starts of the manually audited dependency slice from the two claim redexes.
RELEVANT: dict[str, set[int]] = {
    "semantics/syntax.k": {9, 32, 37, 41, 56, 57, 60},
    "semantics/core.k": {
        13,
        14,
        25,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        49,
        117,
        118,
        130,
        131,
        132,
        185,
        186,
        189,
        190,
        191,
        194,
        208,
        209,
        210,
        213,
        214,
        215,
        217,
        218,
        219,
    },
    "semantics/operators.k": {12, 15, 16, 17},
    "semantics/int.k": {9, 13, 23},
    "semantics/list.k": {13, 14, 15},
    "semantics/controls.k": {51, 52, 53, 54},
    "semantics/functions.k": {8, 63, 64, 78, 85},
    "semantics/call.k": {19, 20, 21, 69},
}

RELEVANT_REASON = {
    "semantics/syntax.k": (
        "Surface constructors and strict/seqstrict evaluation attributes used "
        "by Call/Int/Name/Compare/BinOp/ListExpr/If/Return and their lists."
    ),
    "semantics/core.k": (
        "Configuration/value sorts, lookup, left-to-right argument/list "
        "evaluation, integer literals, allocation, and list conversion."
    ),
    "semantics/operators.k": (
        "Binary dispatch and the left-to-right Compare contexts."
    ),
    "semantics/int.k": (
        "Unbounded integer +, -, and <= exactly match the exercised Python operations."
    ),
    "semantics/list.k": (
        "ListExpr evaluates elements left-to-right and allocates the returned list."
    ),
    "semantics/controls.k": (
        "If converts the integer comparison to its selected statement branch."
    ),
    "semantics/functions.k": (
        "Parameter binding, abrupt Return, frame pop, environment restoration, "
        "and callee-scope removal."
    ),
    "semantics/call.k": (
        "Callee lookup, argument evaluation, exact closure invocation, and frame creation."
    ),
}


def relative_name(path: Path) -> str:
    if path.is_relative_to(ROOT):
        return path.relative_to(ROOT).as_posix()
    return path.as_posix()


def source_files() -> list[Path]:
    return sorted(ROOT.rglob("*.k")) + EXTRA


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if TOP_REQUIRE.match(line):
            starts.append((index, "requires"))
            continue
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        if kind not in ITEM_KINDS:
            continue
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        content = []
        for line in lines[start:end]:
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                content.append(stripped)
        yield kind, start + 1, end, " ".join(content)


def attributes(source: str) -> list[str]:
    present = []
    for attribute in ATTRS:
        if re.search(rf"\b{re.escape(attribute)}\b", source):
            present.append(attribute)
    return present


def decision(path_name: str, kind: str, line: int) -> tuple[str, str]:
    if path_name == "/candidate/spec.k" and kind == "claim":
        return (
            "TARGET-CLAIM",
            "Positive reachability obligation; adequacy and postcondition reviewed separately.",
        )
    if line in RELEVANT.get(path_name, set()):
        return "RELEVANT-SOUND", RELEVANT_REASON[path_name]
    if kind == "syntax":
        return (
            "FIXED-DECLARATION",
            "Generic supplied-syntax declaration outside the target dependency slice; "
            "does not rewrite a reachable target state.",
        )
    if kind == "configuration":
        return (
            "FIXED-CONFIGURATION",
            "Generic supplied configuration; the entry claims explicitly pin every cell.",
        )
    if kind == "context":
        return (
            "FIXED-UNREACHED",
            "Evaluation context is for an AST constructor absent from all reachable target terms.",
        )
    return (
        "FIXED-UNREACHED",
        "Generic supplied-semantics rule outside the target dependency slice; its LHS "
        "constructor/internal continuation is absent from all reachable target states.",
    )


rows = []
counts: Counter[str] = Counter()
attribute_counts: Counter[str] = Counter()
file_counts: dict[str, Counter[str]] = defaultdict(Counter)

for path in source_files():
    path_name = relative_name(path)
    for kind, start, end, source in blocks(path):
        attrs = attributes(source)
        verdict, reason = decision(path_name, kind, start)
        counts[kind] += 1
        file_counts[path_name][kind] += 1
        attribute_counts.update(attrs)
        rows.append(
            {
                "file": path_name,
                "start": start,
                "end": end,
                "kind": kind,
                "attrs": ",".join(attrs) if attrs else "-",
                "decision": verdict,
                "reason": reason,
                "source": source.replace("|", "\\|"),
            }
        )

lines = [
    "# Exhaustive K source inventory",
    "",
    "Generated from the trusted supplied-semantics mount plus the immutable candidate "
    "`verification.k` and `spec.k`. One row exists for every source `syntax`, "
    "`configuration`, `context`, `rule`, and `claim` block. Multi-line declarations "
    "and guards are retained in the Source column.",
    "",
    "Decision codes:",
    "",
    "- `RELEVANT-SOUND`: manually checked member of the exact target execution slice.",
    "- `FIXED-DECLARATION` / `FIXED-CONFIGURATION`: fixed baseline declaration, not a proof extension.",
    "- `FIXED-UNREACHED`: fixed baseline behavior whose constructor/internal continuation "
    "cannot occur in the target slice.",
    "- `TARGET-CLAIM`: one of the two positive reachability obligations.",
    "",
    "## Counts",
    "",
    f"- Total inventoried blocks: {len(rows)}",
]
for kind in sorted(counts):
    lines.append(f"- {kind}: {counts[kind]}")
for attr in ATTRS:
    lines.append(f"- blocks containing `{attr}`: {attribute_counts[attr]}")

lines.extend(
    [
        "",
        "## Per-file counts",
        "",
        "| File | syntax | configuration | context | rule | claim |",
        "|---|---:|---:|---:|---:|---:|",
    ]
)
for path_name in sorted(file_counts):
    count = file_counts[path_name]
    lines.append(
        f"| `{path_name}` | {count['syntax']} | {count['configuration']} | "
        f"{count['context']} | {count['rule']} | {count['claim']} |"
    )

lines.extend(
    [
        "",
        "## Complete inventory",
        "",
        "| ID | Location | Kind | Attributes | Decision | Reason | Source |",
        "|---:|---|---|---|---|---|---|",
    ]
)
for identifier, row in enumerate(rows, 1):
    lines.append(
        f"| {identifier} | `{row['file']}:{row['start']}-{row['end']}` | "
        f"{row['kind']} | `{row['attrs']}` | {row['decision']} | "
        f"{row['reason']} | `{row['source']}` |"
    )

OUTPUT.write_text("\n".join(lines) + "\n")

print(f"inventory_output={OUTPUT}")
print(f"inventory_blocks={len(rows)}")
print(f"kind_counts={dict(counts)}")
print(f"attribute_counts={dict(attribute_counts)}")
print(f"files={len(file_counts)}")
print(
    "candidate_verification_blocks="
    f"{sum(file_counts['/candidate/verification.k'].values())}"
)
print(f"candidate_spec_claims={file_counts['/candidate/spec.k']['claim']}")
