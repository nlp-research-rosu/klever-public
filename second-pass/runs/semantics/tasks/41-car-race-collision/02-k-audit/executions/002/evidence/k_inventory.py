#!/usr/bin/env python3
"""Exhaustive source-level inventory of K directives relevant to the audit."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruct")
paths = (
    [ROOT / "reference-semantics" / "semantics.k"]
    + sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    + [ROOT / "verification.k", ROOT / "spec.k"]
)

directive = re.compile(
    r"^(?P<top_requires>requires)\b|"
    r"^\s*(?P<kind>module|endmodule|imports|syntax|configuration|rule|context|claim|alias)\b"
)
attributes = [
    "function",
    "functional",
    "total",
    "no-evaluators",
    "concrete",
    "simplification",
    "macro",
    "macro-rec",
    "priority",
    "owise",
    "strict",
    "seqstrict",
]

executed_ranges: dict[str, list[tuple[int, int]]] = {
    "reference-semantics/semantics/core.k": [
        (13, 43),
        (49, 60),
        (124, 127),
        (130, 191),
        (194, 194),
        (208, 210),
    ],
    "reference-semantics/semantics/functions.k": [
        (8, 16),
        (63, 90),
    ],
    "reference-semantics/semantics/call.k": [
        (19, 21),
        (69, 75),
    ],
    "reference-semantics/semantics/operators.k": [(12, 12)],
    "reference-semantics/semantics/int.k": [(14, 14)],
    "reference-semantics/semantics/syntax.k": [
        (9, 31),
        (41, 55),
        (56, 61),
    ],
}


def is_executed(relative: str, start: int, end: int) -> bool:
    return any(
        start <= range_end and end >= range_start
        for range_start, range_end in executed_ranges.get(relative, [])
    )


def strip_line_comment(line: str) -> str:
    # Sufficient for these sources: no declaration embeds // inside a K string.
    return line.split("//", 1)[0].rstrip()


items: list[dict[str, object]] = []
for path in paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if directive.match(strip_line_comment(line))
    ]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        match = directive.match(strip_line_comment(lines[start]))
        assert match is not None
        kind = "requires" if match.group("top_requires") else match.group("kind")
        assert kind is not None
        raw_lines = []
        for line in lines[start:end]:
            cleaned = strip_line_comment(line).strip()
            if cleaned:
                raw_lines.append(cleaned)
        text = " ".join(raw_lines)
        bracket_text = " ".join(re.findall(r"\[[^\]]*\]", text))
        flags = [
            name
            for name in attributes
            if re.search(rf"\b{re.escape(name)}\b", bracket_text)
        ]
        relative = path.relative_to(ROOT).as_posix()
        if relative == "verification.k":
            decision = "PROOF_LOCAL_ACCEPTED_EXACT_HARNESS"
            relevance = "proof-local"
        elif relative == "spec.k":
            decision = "TARGET_CLAIM_RESULT_CONSTRAINING"
            relevance = "target-claim"
        elif is_executed(relative, start + 1, end):
            decision = "EXECUTED_FIXED_FRAGMENT_ACCEPTED"
            relevance = "executed-fragment"
        else:
            decision = "UNREACHED_NO_INTENDED_DOMAIN_WITNESS"
            relevance = "unreached"
        if "no-evaluators" in flags:
            decision = "OPAQUE_FIXED_PRIMITIVE_UNREACHED"
            relevance = "unreached-opaque"
        if kind in {"requires", "module", "endmodule", "imports"}:
            decision = "ASSEMBLY_OR_MODULE_DECLARATION"
            relevance = "assembly"
        items.append(
            {
                "path": relative,
                "start": start + 1,
                "end": end,
                "kind": kind,
                "flags": ",".join(flags) or "-",
                "relevance": relevance,
                "decision": decision,
                "text": text,
            }
        )

counts = Counter(str(item["kind"]) for item in items)
decisions = Counter(str(item["decision"]) for item in items)
flag_counts = Counter()
for item in items:
    for flag in str(item["flags"]).split(","):
        if flag != "-":
            flag_counts[flag] += 1
print(f"# item_count={len(items)}")
print("# kind_counts=" + repr(dict(sorted(counts.items()))))
print("# attribute_counts=" + repr(dict(sorted(flag_counts.items()))))
print("# decision_counts=" + repr(dict(sorted(decisions.items()))))
print("id\tpath\tlines\tkind\tattributes\trelevance\tdecision\tdeclaration")
for identifier, item in enumerate(items, 1):
    print(
        "\t".join(
            [
                f"K{identifier:04d}",
                str(item["path"]),
                f"{item['start']}-{item['end']}",
                str(item["kind"]),
                str(item["flags"]),
                str(item["relevance"]),
                str(item["decision"]),
                str(item["text"]).replace("\t", " "),
            ]
        )
    )
