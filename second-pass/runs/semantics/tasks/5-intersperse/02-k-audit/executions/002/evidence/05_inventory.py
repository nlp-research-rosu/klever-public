#!/usr/bin/env python3
"""Emit an exhaustive source-level inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
from pathlib import Path


roots = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

starter = re.compile(
    r"^(module|imports|configuration|syntax|context|rule|claim|endmodule)\b"
)

totals: collections.Counter[str] = collections.Counter()
per_file: dict[str, collections.Counter[str]] = {}

for path in roots:
    lines = path.read_text(encoding="utf-8").splitlines()
    records: list[tuple[int, str, list[str]]] = []
    current: tuple[int, str, list[str]] | None = None

    for line_number, raw in enumerate(lines, 1):
        stripped = raw.strip()
        match = starter.match(stripped)
        top_requires = raw.startswith("requires ")
        if match or top_requires:
            if current is not None:
                records.append(current)
            kind = "requires" if top_requires else match.group(1)
            current = (line_number, kind, [stripped])
        elif current is not None:
            if stripped and not stripped.startswith("//"):
                current[2].append(stripped)
    if current is not None:
        records.append(current)

    counts: collections.Counter[str] = collections.Counter()
    print(f"FILE {path}")
    for index, (line_number, kind, parts) in enumerate(records, 1):
        text = " ".join(parts)
        text = re.sub(r"\s+", " ", text)
        attrs = re.findall(r"\[([^\]]+)\]", text)
        flags: list[str] = []
        if kind == "syntax":
            flags.append("declaration")
            if any("function" in attr.split(",") for attr in attrs):
                flags.append("function")
            if "functional" in text:
                flags.append("functional")
            if "total" in text:
                flags.append("total")
            if "symbol(" in text or "no-evaluators" in text:
                flags.append("opaque-symbol")
            if "macro" in text:
                flags.append("macro")
            if "strict" in text:
                flags.append("evaluation-attribute")
        elif kind == "rule":
            flags.append("operational" if "<k>" in text else "equational")
            if "priority(" in text:
                flags.append("priority")
            if "concrete" in text:
                flags.append("concrete")
            if "simplification" in text or "simplify" in text:
                flags.append("simplification")
            if "[owise]" in text:
                flags.append("owise")
        elif kind == "claim":
            flags.append("reachability-claim")
        elif kind == "context":
            flags.append("evaluation-context")

        counts[kind] += 1
        totals[kind] += 1
        for flag in flags:
            counts[flag] += 1
            totals[flag] += 1
        print(
            f"  {index:03d} {path}:{line_number} "
            f"KIND={kind} FLAGS={','.join(flags) if flags else '-'} TEXT={text}"
        )
    per_file[str(path)] = counts
    print(
        "  FILE_COUNTS "
        + " ".join(f"{key}={counts[key]}" for key in sorted(counts))
    )

print("GLOBAL_COUNTS " + " ".join(f"{key}={totals[key]}" for key in sorted(totals)))
print("SIMPLIFICATION_RULE_COUNT", totals["simplification"])
print("FUNCTIONAL_DECLARATION_COUNT", totals["functional"])
