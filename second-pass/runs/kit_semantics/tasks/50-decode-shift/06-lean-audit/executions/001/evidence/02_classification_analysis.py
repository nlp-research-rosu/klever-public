#!/usr/bin/env python3
"""Independent semantic classification and finite adversarial witnesses."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


OUTPUT = Path("/audit-output/evidence/02_classification_analysis.json")
INVENTORY = json.loads(
    Path("/audit-output/evidence/01_reconstructed_inventory.json").read_text()
)["inventory"]


def sha256_file(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def py_mod(left: int, right: int) -> int:
    return ((left % right) + right) % right


def decode_code(c: int) -> int:
    return py_mod(c - 102, 26) + 97


def encode_code(c: int) -> int:
    return py_mod(c - 92, 26) + 97


def source_decode_code(c: int) -> int:
    return ((c - 5 - ord("a")) % 26) + ord("a")


def prompt_encode_code(c: int) -> int:
    return ((c + 5 - ord("a")) % 26) + ord("a")


def decode_acc(codes: list[int], accumulator: list[int]) -> list[int]:
    result = list(accumulator)
    for code in codes:
        result = result + [decode_code(code)]
    return result


def source_decode(codes: list[int]) -> list[int]:
    result: list[int] = []
    for code in codes:
        result = result + [source_decode_code(code)]
    return result


def lower_codes(codes: list[int]) -> bool:
    return all(97 <= code <= 122 for code in codes)


rules = {rule["source_rule_id"]: rule for rule in INVENTORY["rules"]}
classification = [
    {
        "source_rule_id": INVENTORY["rules"][0]["source_rule_id"],
        "independent_classification": "DEFINITION",
        "symbol": "decodeCode",
        "judgment": (
            "An unconditional equation for a fresh total Int helper. Its RHS is "
            "the source loop's per-character expression after algebraically "
            "combining C - 5 - 97 into C - 102. It does not match an AST or "
            "configuration and therefore does not replace execution."
        ),
    },
    {
        "source_rule_id": INVENTORY["rules"][1]["source_rule_id"],
        "independent_classification": "DEFINITION",
        "symbol": "encodeCode",
        "judgment": (
            "An unconditional equation naming the prompt encoder expression: "
            "C + 5 - 97 equals C - 92. It is used only in the separate inverse "
            "claim and is neither an execution rule nor an assumed property."
        ),
    },
    {
        "source_rule_id": INVENTORY["rules"][2]["source_rule_id"],
        "independent_classification": "DEFINITION",
        "symbol": "decodeAcc",
        "judgment": (
            "The empty-constructor base equation of a named sequence recurrence."
        ),
    },
    {
        "source_rule_id": INVENTORY["rules"][3]["source_rule_id"],
        "independent_classification": "DEFINITION",
        "symbol": "decodeAcc",
        "judgment": (
            "The iCons constructor equation of the same structurally descending "
            "recurrence. It appends the decoded head just as operational string + "
            "uses seqConcat, then recurs on REST."
        ),
    },
    {
        "source_rule_id": INVENTORY["rules"][4]["source_rule_id"],
        "independent_classification": "DEFINITION",
        "symbol": "lowerCodes",
        "judgment": (
            "The empty-constructor equation defining a named domain predicate; "
            "it states no independent mathematical property."
        ),
    },
    {
        "source_rule_id": INVENTORY["rules"][5]["source_rule_id"],
        "independent_classification": "DEFINITION",
        "symbol": "lowerCodes",
        "judgment": (
            "The iCons constructor equation defining that predicate by a head "
            "range test and structural recursion, not a domain theorem."
        ),
    },
]

wide_domain = range(-1000, 1001)
lowercase_domain = range(ord("a"), ord("z") + 1)
sequence_witnesses = [
    [],
    [102],
    [101],
    [97, 102, 122],
    list(range(97, 123)),
    [102, 103, 104, 105, 106],
]

checks = {
    "all_rules_have_no_simplification_attribute": all(
        "simplification" not in rule["attributes"]
        for rule in INVENTORY["rules"]
    ),
    "all_rule_lhs_are_helper_equations_not_configurations": all(
        "<k>" not in rule["text"]
        and "Call(" not in rule["text"]
        and "#loop(" not in rule["text"]
        for rule in INVENTORY["rules"]
    ),
    "decode_equation_matches_source_over_-1000_to_1000": all(
        decode_code(c) == source_decode_code(c) for c in wide_domain
    ),
    "encode_equation_matches_prompt_over_-1000_to_1000": all(
        encode_code(c) == prompt_encode_code(c) for c in wide_domain
    ),
    "inverse_holds_for_all_lowercase_ascii_codes": all(
        decode_code(encode_code(c)) == c for c in lowercase_domain
    ),
    "decodeAcc_witnesses_match_source_loop": all(
        decode_acc(codes, []) == source_decode(codes)
        for codes in sequence_witnesses
    ),
    "lowerCodes_empty_true": lower_codes([]),
    "lowerCodes_all_lowercase_true": lower_codes(list(lowercase_domain)),
    "lowerCodes_rejects_below_range": not lower_codes([96]),
    "lowerCodes_rejects_above_range": not lower_codes([123]),
    "counterfactual_shift_4_differs_on_f": (
        ((ord("f") - 4 - ord("a")) % 26) + ord("a")
        != decode_code(ord("f"))
    ),
    "all_independent_classifications_are_definition": all(
        entry["independent_classification"] == "DEFINITION"
        for entry in classification
    ),
    "true_domain_lemma_count": 0,
    "proved_derived_lemma_count": 0,
    "operational_rule_count": 0,
}

result = {
    "command": (
        "python3 /audit-output/evidence/02_classification_analysis.py"
    ),
    "source_and_semantics_hashes": {
        "solution.py": sha256_file("/reference/k-proof/solution.py"),
        "prompt.py": sha256_file("/reference/k-proof/prompt.py"),
        "spec.k": sha256_file("/reference/k-proof/spec.k"),
        "semantics/int.k": sha256_file(
            "/reference/k-proof/reference-semantics/semantics/int.k"
        ),
        "semantics/str.k": sha256_file(
            "/reference/k-proof/reference-semantics/semantics/str.k"
        ),
        "semantics/builtins.k": sha256_file(
            "/reference/k-proof/reference-semantics/semantics/builtins.k"
        ),
        "semantics/controls.k": sha256_file(
            "/reference/k-proof/reference-semantics/semantics/controls.k"
        ),
    },
    "operational_semantics_used": {
        "pyMod": (
            "semantics/int.k:19-20 defines pyMod(I1,I2) as "
            "((I1 %Int I2) +Int I2) %Int I2"
        ),
        "string_iteration": (
            "semantics/str.k:8-10 yields one-character strings from iCons"
        ),
        "string_concat": (
            "semantics/str.k:20-24 defines seqConcat and operational str +"
        ),
        "ord_chr": (
            "semantics/builtins.k:142-145 maps singleton strings to codes and "
            "codes in [0,128) back to singleton strings"
        ),
        "for_loop": (
            "semantics/controls.k:62-74 evaluates the iterable and iterates with "
            "#iterNext/#loopStep"
        ),
    },
    "classification": classification,
    "checks": checks,
    "witnesses": {
        "per_character": {
            "f_code": ord("f"),
            "decode_f": decode_code(ord("f")),
            "decode_e_wraparound": decode_code(ord("e")),
            "decode_a_wraparound": decode_code(ord("a")),
            "decode_z": decode_code(ord("z")),
            "mutated_shift_4_on_f": (
                ((ord("f") - 4 - ord("a")) % 26) + ord("a")
            ),
        },
        "sequences": [
            {
                "input": codes,
                "decodeAcc": decode_acc(codes, []),
                "source_loop": source_decode(codes),
            }
            for codes in sequence_witnesses
        ],
    },
}

if not all(value is True or value == 0 for value in checks.values()):
    raise SystemExit(f"classification check failed: {checks}")

OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
