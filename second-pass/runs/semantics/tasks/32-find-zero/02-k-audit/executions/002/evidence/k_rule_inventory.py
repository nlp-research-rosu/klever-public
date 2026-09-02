#!/usr/bin/env python3
"""Exhaustive top-level K declaration/rule inventory with path-use classification."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
OUTPUT = Path("/audit-output/evidence/stage5-rule-inventory.json")
START = re.compile(
    r"^(?:requires|module|endmodule)\b"
    r"|^  (?:imports|configuration|syntax|context|rule|claim|alias)\b"
)

MATERIAL_MODULES = {
    "semantics.k",
    "syntax.k",
    "core.k",
    "iter.k",
    "operators.k",
    "int.k",
    "bool.k",
    "float.k",
    "list.k",
    "tuple.k",
    "comprehension.k",
    "controls.k",
    "functions.k",
    "builtins.k",
    "call.k",
    "verification.k",
    "spec.k",
}


def kind_of(block: str) -> str:
    first = block.lstrip().split(None, 1)[0] if block.strip() else "unknown"
    return first


def attributes(block: str) -> list[str]:
    found: list[str] = []
    for bracket in re.findall(r"\[([^\]]+)\]", block, flags=re.DOTALL):
        found.extend(part.strip() for part in bracket.split(","))
    return found


def inventory_file(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    starts: list[int] = []
    for index, line in enumerate(lines):
        if START.match(line) and not line.lstrip().startswith("//"):
            starts.append(index)
    entries: list[dict[str, object]] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        block = "\n".join(block_lines)
        kind = kind_of(block)
        relative = str(path.relative_to(ROOT))
        candidate_local = path.name in {"verification.k", "spec.k"}
        decision = ""
        rationale = ""
        if relative == "verification.k":
            if start + 1 in {9, 10, 24, 25, 36, 37, 55, 56, 63, 64}:
                decision = "ACCEPT_MACRO_IDENTITY"
                rationale = (
                    "Pure syntax/macro expansion; mechanical constructor comparison "
                    "confirms the submitted bodies after expansion."
                )
            elif start + 1 == 78:
                decision = "FATAL_UNJUSTIFIED_OPAQUE_PRECONDITION"
                rationale = (
                    "validPolynomial has no equations or connection theorem, so no "
                    "source-contract input is proved to satisfy it."
                )
            elif start + 1 == 81:
                decision = "FATAL_UNJUSTIFIED_RESULT_ABSTRACTION"
                rationale = (
                    "Four fresh result-bearing constructors are unconstrained and later "
                    "control the returned value/postcondition."
                )
            elif start + 1 == 89:
                decision = "FATAL_UNCONNECTED_POSTCONDITION_SYMBOL"
                rationale = (
                    "The predicate has no independent mathematical definition connecting "
                    "a Val to polynomial evaluation."
                )
            elif start + 1 == 90:
                decision = "FATAL_ANSWER_ENCODING"
                rationale = (
                    "Constructor shape alone rewrites the claimed correctness predicate "
                    "to true; the opposite interpretation witness returns 0 for [1,2]."
                )
            elif start + 1 in {95, 96}:
                decision = "CONDITIONALLY_ACCEPT_ADMINISTRATIVE"
                rationale = (
                    "The continuation is an ordinary forwarding rule, but its conclusion "
                    "depends entirely on the illegitimate approximatesZero definition."
                )
            elif start + 1 in {103, 117}:
                decision = "FATAL_UNSOUND_OPERATIONAL_BRIDGE"
                rationale = (
                    "Priority bridge skips real loop execution without a bridge-free "
                    "connection theorem; concrete and bridge-free witnesses disagree."
                )
            else:
                decision = "ACCEPT_STRUCTURAL"
                rationale = "File/module/import structure only."
        elif relative == "spec.k":
            if kind == "claim":
                decision = "FATAL_INADEQUATE_TARGET_CLAIM"
                rationale = (
                    "The claim invokes a direct closure in an empty module scope and "
                    "constrains only an opaque constructor/tautological predicate."
                )
            else:
                decision = "ACCEPT_STRUCTURAL"
                rationale = "File/module/import structure only."
        elif path.name in MATERIAL_MODULES:
            decision = "ACCEPT_FIXED_REVIEWED_MATERIAL_PATH"
            rationale = (
                "Byte-identical trusted supplied semantics. This declaration/rule is in "
                "a module needed to declare or execute submitted source constructs; the "
                "used-path mapping and concrete LLVM checks found no candidate-local change."
            )
        else:
            decision = "ACCEPT_FIXED_INERT_FOR_THIS_PROGRAM"
            rationale = (
                "Byte-identical trusted supplied semantics in a module not used by any "
                "submitted source construct; it cannot contribute to these claim closures."
            )

        entry = {
            "file": relative,
            "start_line": start + 1,
            "end_line": start + len(block_lines),
            "kind": kind,
            "attributes": attributes(block),
            "text": block,
            "candidate_local": candidate_local,
            "material_source_construct_module": path.name in MATERIAL_MODULES,
            "review_decision_group": (
                "candidate-proof-extension-or-claim"
                if path.name in {"verification.k", "spec.k"}
                else (
                    "trusted-supplied-semantics-material-path"
                    if path.name in MATERIAL_MODULES
                    else "trusted-supplied-semantics-unused-by-solution"
                )
            ),
            "audit_decision": decision,
            "audit_rationale": rationale,
        }
        entries.append(entry)
    return entries


def main() -> int:
    files = [ROOT / "reference-semantics" / "semantics.k"]
    files.extend(sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")))
    files.extend([ROOT / "verification.k", ROOT / "spec.k"])
    entries: list[dict[str, object]] = []
    for path in files:
        entries.extend(inventory_file(path))
    counts = collections.Counter(str(entry["kind"]) for entry in entries)
    group_counts = collections.Counter(
        str(entry["review_decision_group"]) for entry in entries
    )
    payload = {
        "scope": [str(path.relative_to(ROOT)) for path in files],
        "entry_count": len(entries),
        "kind_counts": dict(sorted(counts.items())),
        "decision_group_counts": dict(sorted(group_counts.items())),
        "entries": entries,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"inventory output: {OUTPUT}")
    print(f"files inventoried: {len(files)}")
    print(f"top-level entries: {len(entries)}")
    print(f"kind counts: {dict(sorted(counts.items()))}")
    print(f"decision groups: {dict(sorted(group_counts.items()))}")
    print("candidate-local entries:")
    for entry in entries:
        if entry["candidate_local"]:
            text = str(entry["text"]).splitlines()[0]
            print(
                f"  {entry['file']}:{entry['start_line']}-{entry['end_line']} "
                f"{entry['kind']}: {text.strip()}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
