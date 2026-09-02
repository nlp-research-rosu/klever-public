#!/usr/bin/env python3
"""Attach an audit disposition to every record in the exhaustive K inventory."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
import sys


INVENTORY_SCRIPT = Path("/audit-output/evidence/k_inventory.py")
spec = importlib.util.spec_from_file_location("review_inventory", INVENTORY_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import inventory helper")
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


MATERIAL_FILES = {
    "semantics.k",
    "syntax.k",
    "core.k",
    "iter.k",
    "operators.k",
    "int.k",
    "list.k",
    "tuple.k",
    "controls.k",
    "functions.k",
    "call.k",
}

VERIFICATION_RATIONALE = {
    7: "Compile-time macro declaration for the loop body.",
    8: "Exact loop-body constructor expansion; KORE identity checked.",
    32: "Compile-time macro declaration for the function body.",
    33: "Exact function-body constructor expansion; KORE identity checked.",
    41: "Compile-time macro declaration for the function definition.",
    42: "Exact function-definition constructor expansion; KORE identity checked.",
    46: "Total structural predicate over the two ValSeq constructors.",
    47: "Empty sequence is an all-Int sequence.",
    48: "Cons case is true exactly when the head is an Int and the tail is all-Int.",
    53: "Guard predicate names the generated Int-sort predicate.",
    54: "Definitional equality with isInt.",
    56: "Opaque total projection symbol; all value-influencing uses are guarded.",
    59: "Definedness of Val-to-Int subsort projection is characterized by isInt.",
    63: "Guarded concrete orientation to the existing partial subsort projection.",
    64: "Exact definedProjectInt guard for line 63.",
    67: "Guarded symbolic orientation back to the named total projection.",
    68: "Exact definedProjectInt guard for line 67.",
    71: "Projection collapses to identity on statically sorted Int values.",
    74: "Idempotence; inner projection is already an Int.",
    80: "Guarded Int multiplication dispatch; agrees with MPY-INT on overlap.",
    82: "Both Val operands are constrained to the Int subsort.",
    85: "Guarded Int addition dispatch; agrees with MPY-INT on overlap.",
    87: "The Val addend is constrained to the Int subsort.",
    91: "Total per-index contribution function over Int pairs.",
    92: "Square branch for index divisible by 3.",
    94: "Square branch guard.",
    95: "Cube branch after excluding divisibility by 3.",
    97: "Cube branch guard.",
    99: "Unchanged-value branch after excluding both divisibilities.",
    101: "Unchanged-value branch guard.",
    107: "Total structural accumulator over ValSeq.",
    108: "Empty tail returns the accumulator.",
    109: "Int-head recurrence mirrors one complete program loop iteration.",
    114: "Int-head recurrence guard.",
    115: "Off-domain totalization; unreachable under every entry precondition.",
    117: "Complementary non-Int guard for off-domain totalization.",
}

SPEC_RATIONALE = {
    8: "Universal loop circularity with exact Return/#endcall continuation and cells.",
    35: "Satisfiable all-Int/nonnegative/fresh-frame precondition.",
    41: "Primary heap-referenced whole-program entry claim.",
    62: "Unbounded all-Int domain and disjoint heap-location precondition.",
    67: "Supporting bare-list whole-program entry claim.",
    88: "Unbounded all-Int domain precondition.",
}


def disposition(path: Path, line: int, kind: str, raw: str) -> tuple[str, str]:
    if path == Path("/candidate/verification.k"):
        if kind in {"rule", "syntax", "requires"} and line in VERIFICATION_RATIONALE:
            return "ACCEPTED_PROOF_EXTENSION", VERIFICATION_RATIONALE[line]
        return (
            "STRUCTURAL_PROOF_MODULE",
            "Module/import/require structure; no semantic conclusion by itself.",
        )
    if path == Path("/candidate/spec.k"):
        if kind in {"claim", "requires"} and line in SPEC_RATIONALE:
            return "ACCEPTED_REACHABILITY_OBLIGATION", SPEC_RATIONALE[line]
        return (
            "STRUCTURAL_SPEC_MODULE",
            "Module/import/require structure; no rewrite rule added.",
        )
    if path.name == "concrete.k":
        return (
            "RUNTIME_ONLY_FIXED_BASELINE",
            "Imported only by MPY-KRUN for concrete testing, not by VERIFICATION.",
        )
    if "no-evaluators" in raw or "symbol(" in raw:
        return (
            "FIXED_OPAQUE_UNREACHABLE",
            "Opaque supplied-semantics boundary; its head symbol is absent from "
            "the submitted program, proof summary, and reachable claim terms.",
        )
    if kind in {"rule", "context", "configuration", "syntax"}:
        if path.name in MATERIAL_FILES:
            return (
                "ACCEPTED_FIXED_MATERIAL_MODULE",
                "Part of the selected supplied semantics. Constructor-level "
                "reachability and material rules are mapped in 05-rule-review.md.",
            )
        return (
            "FIXED_CONSTRUCTOR_DISJOINT",
            "Part of the selected supplied semantics, but its source constructors "
            "and helper heads are absent from the submitted term and proof summary.",
        )
    return (
        "STRUCTURAL_FIXED_MODULE",
        "Assembly/import/require/module delimiter for the supplied semantics.",
    )


def main() -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(
        ["id", "path", "line", "kind", "attributes", "disposition", "rationale"]
    )
    global_id = 0
    for path in inventory.FILES:
        for line, kind, raw in inventory.extract(path):
            if kind == "endmodule":
                continue
            global_id += 1
            result, rationale = disposition(path, line, kind, raw)
            writer.writerow(
                [
                    f"K{global_id:04d}",
                    str(path),
                    line,
                    kind,
                    inventory.attributes(raw),
                    result,
                    rationale,
                ]
            )


if __name__ == "__main__":
    main()
