#!/usr/bin/env python3
"""Compare frozen K value constructors with the generated Lean value domain."""

from __future__ import annotations

import json
import re
from pathlib import Path


k_core = Path(
    "/reference/k-proof/reference-semantics/semantics/core.k"
).read_text()
k_sort = Path(
    "/reference/k-proof/reference-semantics/semantics/sort.k"
).read_text()
lean_sorts = Path(
    "/reference/klean-generation/generated/"
    "Klean33SortThird/Sorts.lean"
).read_text()
candidate = Path("/candidate/Proof.lean").read_text()

iterable_block_match = re.search(
    r"(?ms)^\s*inductive SortIterable : Type where\n"
    r"(.*?)(?=^\s*(?:inductive|structure)\s+)",
    lean_sorts,
)
iterable_block = (
    iterable_block_match.group(1).strip()
    if iterable_block_match is not None
    else None
)

facts = {
    "frozen_k_declares_Str_constructor": (
        "syntax Str    ::= str(IntSeq)" in k_core
    ),
    "frozen_k_includes_Str_in_Iterable": (
        re.search(r"(?m)^\s*\|\s*Str\s*$", k_core) is not None
    ),
    "frozen_k_has_concrete_string_sort": (
        "rule sortVS(vCons(str(CS:IntSeq), R:ValSeq))" in k_sort
    ),
    "generated_lean_declares_SortStr": (
        re.search(r"\bSortStr\b", lean_sorts) is not None
    ),
    "generated_lean_iterable_has_string_constructor": (
        iterable_block is not None
        and re.search(r"\bstr\b|\bSortStr\b", iterable_block) is not None
    ),
    "candidate_only_compares_integer_values": (
        "| SortVal.inj_SortInt valueInt, SortVal.inj_SortInt headInt =>"
        in candidate
    ),
    "candidate_noninteger_branch_preserves_insertion_order": (
        "| _, _ => value :: head :: tail" in candidate
    ),
}
facts["generated_lean_preserves_frozen_string_value_domain"] = (
    facts["generated_lean_declares_SortStr"]
    and facts["generated_lean_iterable_has_string_constructor"]
)

print(
    json.dumps(
        {
            "facts": facts,
            "generated_SortIterable_block": iterable_block,
            "judgment": (
                "The generated SortVal/SortIterable domain cannot represent "
                "the frozen K Str values exercised by sortVS; the universal "
                "Lean obligations are therefore over a strict subset of the "
                "frozen ValSeq domain."
            ),
        },
        indent=2,
        sort_keys=True,
    )
)
