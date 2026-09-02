#!/usr/bin/env python3
"""Reconcile the exact #print axioms output with the generated trust ledger."""

from __future__ import annotations

import json
from pathlib import Path


ACTUAL = {
    "«Float2Int(_)_FLOAT_Int_Float»",
    "«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int»",
    "«Int2String(_)_STRING-COMMON_String_Int»",
    "«_%Int_»",
    "«_*Float__FLOAT_Float_Float_Float»",
    "«_+Float__FLOAT_Float_Float_Float»",
    "«_-Float__FLOAT_Float_Float_Float»",
    "«_/Float__FLOAT_Float_Float_Float»",
    "«_<Float__FLOAT_Bool_Float_Float»",
    "«_==Bool_»",
    "«_==Float_»",
    "«_==K_»",
    "«_==String__STRING-COMMON_Bool_String_String»",
    "«_>=Float__FLOAT_Bool_Float_Float»",
    "«_>Float__FLOAT_Bool_Float_Float»",
    "«_^Float__FLOAT_Float_Float_Float»",
    "«_^Int_»",
    "«absFloat(_)_FLOAT_Float_Float»",
    "«absInt(_)_INT-COMMON_Int_Int»",
    "append",
    "«binAcc(_,_)_MPY-BUILTINS_IntSeq_Int_IntSeq»",
    "«buildVS(_,_,_,_)_MPY-SUBSCRIPT_ValSeq_ValSeq_Int_Int_Int»",
    "«ceilFloat(_)_FLOAT_Float_Float»",
    "«cntSub(_,_)_MPY-METHODS_Int_IntSeq_IntSeq»",
    "«floorFloat(_)_FLOAT_Float_Float»",
    "«maxFloat(_,_)_FLOAT_Float_Float_Float»",
    "md5hexCodes",
    "«minFloat(_,_)_FLOAT_Float_Float_Float»",
    "propext",
    "«rootFloat(_,_)_FLOAT_Float_Float_Int»",
    "sortKeyVS",
    "«strToCodes(_)_MPY-STR_IntSeq_String»",
    "Classical.choice",
    "Quot.sound",
}

CORE = {"propext", "Classical.choice", "Quot.sound"}


def main() -> None:
    inventory = json.loads(
        Path("/reference/klean-generation/trust-inventory.json").read_text()
    )
    recorded = {entry["name"] for entry in inventory["allowlist"]}
    generated_dependencies = ACTUAL - CORE
    unrecorded = generated_dependencies - recorded
    print(f"actual_dependency_count={len(ACTUAL)}")
    print(f"standard_Lean_core_axioms={sorted(CORE)}")
    print(f"generated_dependency_count={len(generated_dependencies)}")
    print(f"recorded_generated_dependencies={sorted(generated_dependencies)}")
    print(f"unrecorded_generated_dependencies={sorted(unrecorded)}")
    print(f"sorryAx_present={'sorryAx' in ACTUAL}")
    print(
        "RESULT="
        + (
            "PASS"
            if not unrecorded
            and "sorryAx" not in ACTUAL
            and inventory["designated_sorries"] == 0
            and inventory["other_sorries"] == 0
            else "FAIL"
        )
    )


if __name__ == "__main__":
    main()
