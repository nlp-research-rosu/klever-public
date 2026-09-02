#!/usr/bin/env python3
"""Produce an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import collections
import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/86-anti-shuffle")
OUTPUT = Path("/audit-output/evidence/k_inventory.tsv")
START = re.compile(
    r"^(requires)\b|^\s*(module|endmodule|imports|configuration|syntax|rule|context|claim|alias)\b"
)
MODULE = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")


def source_files() -> list[Path]:
    semantics_root = ROOT / "reference-semantics"
    return sorted(semantics_root.rglob("*.k")) + [ROOT / "verification.k", ROOT / "spec.k"]


def kind_for(keyword: str, body: str) -> str:
    attributes: list[str] = []
    if "[function" in body or re.search(r"\bfunction\b", body):
        attributes.append("function")
    if re.search(r"\btotal\b", body):
        attributes.append("total")
    if re.search(r"\bfunctional\b", body):
        attributes.append("functional")
    if "no-evaluators" in body:
        attributes.append("opaque/no-evaluators")
    if "[simplification" in body:
        attributes.append("simplification")
    if "[concrete" in body:
        attributes.append("concrete")
    priority = re.search(r"priority\(([^)]+)\)", body)
    if priority:
        attributes.append(f"priority({priority.group(1)})")
    if "[owise" in body:
        attributes.append("owise")
    return keyword + (":" + ",".join(attributes) if attributes else "")


def decision_for(path: Path, keyword: str, start: int, body: str) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative.startswith("reference-semantics/"):
        if "no-evaluators" in body:
            return "ACCEPTED_FIXED_SEMANTICS_OPAQUE_TRUST_BOUNDARY_UNUSED_BY_TARGET"
        if relative.endswith("semantics/concrete.k"):
            return "ACCEPTED_FIXED_CONCRETE_SEMANTICS_NOT_IN_PROOF_MODULE"
        return "ACCEPTED_FIXED_SUPPLIED_SEMANTICS"
    if relative == "spec.k" and keyword == "claim":
        return "AUDITED_RESULT_CONSTRAINING_REACHABILITY_CLAIM"
    if relative == "verification.k":
        if start in {9, 16}:
            return "AUDITED_SOUND_DERIVED_SIMPLIFICATION"
        if start in {26, 27, 30, 34}:
            return "AUDITED_SOUND_INSERT_SUMMARY_COMPLETE_DISJOINT_DESCENDING"
        if start in {41, 42, 45, 51}:
            return "AUDITED_SOUND_OUTER_SUMMARY_COMPLETE_DISJOINT_DESCENDING"
        if start in {56, 57, 58}:
            return "AUDITED_SOUND_ASCII_DOMAIN_PREDICATE"
        if start == 69:
            return "UNSOUND_OPERATIONAL_BRIDGE_UNPINNED_CONTINUATION_COUNTEREXAMPLE"
        if start == 111:
            return "UNSOUND_OPERATIONAL_BRIDGE_UNPINNED_CONTINUATION_COUNTEREXAMPLE"
        return "AUDITED_PROOF_LOCAL_MODULE_STRUCTURE"
    return "REVIEWED"


def declarations(path: Path):
    lines = path.read_text().splitlines()
    module = "<outside-module>"
    starts: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines, 1):
        match = START.match(line)
        if not match:
            continue
        keyword = match.group(1) or match.group(2)
        starts.append((index, keyword, module))
        module_match = MODULE.match(line)
        if module_match:
            module = module_match.group(1)
        elif keyword == "endmodule":
            module = "<outside-module>"

    for position, (start, keyword, declaration_module) in enumerate(starts):
        end = starts[position + 1][0] - 1 if position + 1 < len(starts) else len(lines)
        body_lines = lines[start - 1 : end]
        while body_lines and (not body_lines[-1].strip() or body_lines[-1].lstrip().startswith("//")):
            body_lines.pop()
            end -= 1
        body = " ".join(part.strip() for part in body_lines if part.strip())
        yield {
            "source": path.relative_to(ROOT).as_posix(),
            "module": declaration_module,
            "start_line": start,
            "end_line": end,
            "kind": kind_for(keyword, body),
            "decision": decision_for(path, keyword, start, body),
            "declaration": body,
        }


def main() -> int:
    rows = [row for path in source_files() for row in declarations(path)]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "source",
                "module",
                "start_line",
                "end_line",
                "kind",
                "decision",
                "declaration",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    kinds = collections.Counter(row["kind"].split(":", 1)[0] for row in rows)
    decisions = collections.Counter(row["decision"] for row in rows)
    print(f"source_files={len(source_files())}")
    print(f"inventory_rows={len(rows)}")
    print(f"kinds={dict(sorted(kinds.items()))}")
    print(f"decisions={dict(sorted(decisions.items()))}")
    print(f"output={OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
