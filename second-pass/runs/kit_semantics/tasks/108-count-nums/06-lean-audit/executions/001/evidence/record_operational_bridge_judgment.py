#!/usr/bin/env python3
"""Record the independent per-parameter operational bridge comparison."""

from __future__ import annotations

import json
from pathlib import Path


manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)

judgments = {
    "«_-Int_»": {
        "candidate_lines": "136",
        "frozen_semantics": ["reference-semantics/semantics/int.k:7"],
        "assessment": (
            "x - y is Lean integer subtraction and exactly realizes K _-Int_; "
            "7-3=4 separates it from the identity counterfactual."
        ),
    },
    "_andBool_": {
        "candidate_lines": "138",
        "frozen_semantics": ["verification.k:65-66"],
        "assessment": (
            "Bool && is K andBool on the two guard booleans; true&&false=false "
            "separates it from a constant-true guard."
        ),
    },
    "«_>=Int_»": {
        "candidate_lines": "140",
        "frozen_semantics": ["verification.k:60,66,77"],
        "assessment": (
            "decide (x ≥ y) is the exact K >=Int predicate; -2>=0=false "
            "separates it from a vacuous guard."
        ),
    },
    "«_<Int_»": {
        "candidate_lines": "142",
        "frozen_semantics": [
            "reference-semantics/semantics/int.k:22",
            "verification.k:41-44",
        ],
        "assessment": (
            "decide (x < y) is exact K <Int; the signed true/false examples "
            "exercise both comparison outcomes."
        ),
    },
    "«allDigitCodes(_)_VERIFICATION_Bool_IntSeq»": {
        "candidate_lines": "6-9,144-145",
        "frozen_semantics": ["verification.k:69-72"],
        "assessment": (
            "The candidate structurally recurses over IntSeq and checks both "
            "48≤c and c≤57 for every element. Valid 49,48,53 and invalid 47 "
            "separate it from a constant predicate."
        ),
    },
    "«applyBuiltin(_,_)_MPY-BUILTINS_Val_String_Vals»": {
        "candidate_lines": "124-133,147-148",
        "frozen_semantics": [
            "reference-semantics/semantics/builtins.k:147-149",
            "verification.k:63-67",
        ],
        "assessment": (
            "It agrees on the source-used `str` cases, but the def is bound to "
            "the full applyBuiltin KORE symbol. Frozen builtins.k:140 says "
            "applyBuiltin(\"int\", I, .Vals) => I; the candidate's wildcard "
            "returns noneV for int(3). This is a convenient partial dispatcher, "
            "not the frozen symbol's honest total operational meaning."
        ),
        "full_kore_symbol_agrees": False,
        "counterexample": (
            "applyBuiltin(\"int\", inj_SortInt 3, .Vals): frozen result "
            "inj_SortInt 3; candidate result noneV"
        ),
    },
    "«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»": {
        "candidate_lines": "111-118,150-151",
        "frozen_semantics": [
            "reference-semantics/semantics/int.k:22-27",
            "verification.k:41-44",
        ],
        "assessment": (
            "It implements all integer comparisons and agrees on the cited "
            "source-used '<' case, but the def is bound to the full applyCmp "
            "KORE symbol. Frozen str.k:56 and strLt make \"a\" < \"b\" true; "
            "the candidate wildcard returns false. The public binding therefore "
            "does not implement the frozen dispatcher."
        ),
        "full_kore_symbol_agrees": False,
        "counterexample": (
            "applyCmp(\"<\", str([97]), str([98])): frozen result true; "
            "candidate result false"
        ),
    },
    "«applyUn(_,_)_MPY-CORE_Val_String_Val»": {
        "candidate_lines": "120-122,153-154",
        "frozen_semantics": [
            "reference-semantics/semantics/int.k:7",
            "verification.k:45-48",
        ],
        "assessment": (
            "It agrees on the cited source-used integer '-' case, but the def "
            "is bound to the full applyUn KORE symbol. Frozen bool.k:8 gives "
            "applyUn(\"not\", true) = false; the candidate wildcard returns "
            "noneV. The public binding is only a partial dispatcher."
        ),
        "full_kore_symbol_agrees": False,
        "counterexample": (
            "applyUn(\"not\", inj_SortBool true): frozen result "
            "inj_SortBool false; candidate result noneV"
        ),
    },
    "«decimalCodes(_)_VERIFICATION_IntSeq_Int»": {
        "candidate_lines": "11-16,47-82,156-157",
        "frozen_semantics": [
            "reference-semantics/semantics/builtins.k:148",
            "reference-semantics/semantics/str.k:13-17",
            "verification.k:54-61,74-78",
        ],
        "assessment": (
            "The quotient-first, remainder-last recurrence emits ordinary "
            "base-10 ASCII in order, emits '0' for zero, and prefixes '-' for "
            "negative Int.negSucc values. Evaluations 105→[49,48,53] and "
            "-42→[45,52,50] reject the convenient singleton-'0' definition. "
            "Fuel starts at |n|, which is more than the required decimal divisions."
        ),
    },
    "«definedProjectInt(_)_VERIFICATION_Bool_Val»": {
        "candidate_lines": "96-98,159-160",
        "frozen_semantics": ["verification.k:18-19,24-26"],
        "assessment": (
            "True exactly on SortVal.inj_SortInt and false on other Val "
            "constructors, matching definedProjectInt(V)=>isInt(V). Int and "
            "string cases reject a constant predicate."
        ),
    },
    "isInt": {
        "candidate_lines": "92-94,162",
        "frozen_semantics": [
            "K generated sort predicate for Int < Val < KItem < K",
            "verification.k:41-48,63-67",
        ],
        "assessment": (
            "True exactly for a singleton K sequence containing an injected "
            "integer, the representation used by every generated guard; a "
            "singleton string is false. This rejects constant true."
        ),
    },
    "projectIntTotal": {
        "candidate_lines": "100-105,164",
        "frozen_semantics": ["verification.k:21-37"],
        "assessment": (
            "Projects the integer constructor unchanged on every guarded match. "
            "The chosen 0 outside definedProjectInt is only a totalization of an "
            "operationally undefined/off-guard case and is never used by a cited "
            "rule. Projecting -17 rejects constant-zero on the meaningful domain."
        ),
    },
    "«project:Int?»": {
        "candidate_lines": "107-109,166",
        "frozen_semantics": ["verification.k:24-26"],
        "assessment": (
            "Returns some i exactly for the singleton injected-Int K term and "
            "none otherwise, which preserves partial-cast definedness. Integer "
            "and string cases reject constant none/some implementations."
        ),
    },
}

rows = []
for parameter in manifest["target"]["parameters"]:
    full_symbol_agrees = judgments[parameter["name"]].get(
        "full_kore_symbol_agrees", True
    )
    row = {
        **parameter,
        **judgments[parameter["name"]],
        "candidate_file": "Proof.lean",
        "source_reachable_domain_agrees": True,
        "full_kore_symbol_agrees": full_symbol_agrees,
        "constant_identity_hardcoded_or_vacuous": not full_symbol_agrees,
        "adversarial_test_file": "OperationalAudit.lean",
        "counterfactual_tested": True,
        "judgment": "PASS" if full_symbol_agrees else "FAIL",
    }
    rows.append(row)

result = {
    "parameter_count": len(rows),
    "scope": (
        "Each public total Lean binding was checked both on the source_rule_ids "
        "that caused parameterization and against the operational meaning of "
        "its entire bound kore_symbol. Agreement only on the convenient "
        "source-used dispatcher literal is insufficient for a full-symbol def."
    ),
    "candidate_proof_lines": 201,
    "adversarial_test_exit_code": 0,
    "rows": rows,
    "all_operational_bridges_pass": (
        len(rows) == 13 and all(row["judgment"] == "PASS" for row in rows)
    ),
    "failed_bindings": [
        row["name"] for row in rows if row["judgment"] == "FAIL"
    ],
}
Path(
    "/audit-output/evidence/operational-bridge-judgment.json"
).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
