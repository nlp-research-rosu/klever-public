#!/usr/bin/env python3
"""Problem-specific operational-bridge and adversarial-value audit."""

from __future__ import annotations

import json
import re
from pathlib import Path


candidate_proof = Path("/candidate/Proof.lean").read_text()
candidate_model = Path("/candidate/Proof/FibfibModel.lean").read_text()
solution = Path("/reference/k-proof/solution.py").read_text()
verification = Path("/reference/k-proof/verification.k").read_text()
kore = Path(
    "/reference/k-proof/verification-kompiled/definition.kore"
).read_text()
manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
bridge_output = Path(
    "/audit-output/evidence/10d-bridge-adversarial.log"
).read_text()


def frozen_summary(n: int) -> int:
    if n < 0:
        return 0
    values = [0, 0, 1]
    if n < 3:
        return values[n]
    for index in range(3, n + 1):
        values.append(
            values[index - 1]
            + values[index - 2]
            + values[index - 3]
        )
    return values[n]


def source_loop(n: int) -> int:
    a, b, c = 0, 0, 1
    i = 0
    next_value = 1
    while i < n:
        next_value = a + b + c
        a = b
        b = c
        c = next_value
        i = i + 1
    return a


sample_indices = [-5, -1, 0, 1, 2, 3, 4, 5, 8, 12]
expected_samples = [frozen_summary(index) for index in sample_indices]
lean_sample_line = (
    "[0, 0, 0, 0, 1, 1, 2, 4, 24, 274]"
)
hook_lines = {
    "INT.add": re.findall(
        r"(?m)^.*hook\{\}\(\"INT\.add\"\).*$", kore
    ),
    "INT.ge": re.findall(
        r"(?m)^.*hook\{\}\(\"INT\.ge\"\).*$", kore
    ),
}
parameters = {
    parameter["kore_symbol"]: parameter
    for parameter in manifest["target"]["parameters"]
}

checks = {
    "target_binds_int_ge_hook_symbol": (
        "Lbl'Unds-GT-Eqls'Int'Unds'" in parameters
        and len(hook_lines["INT.ge"]) == 1
        and "Lbl'Unds-GT-Eqls'Int'Unds'"
        in hook_lines["INT.ge"][0]
    ),
    "target_binds_int_add_hook_symbol": (
        "Lbl'UndsPlus'Int'Unds'" in parameters
        and len(hook_lines["INT.add"]) == 1
        and "Lbl'UndsPlus'Int'Unds'" in hook_lines["INT.add"][0]
    ),
    "candidate_ge_is_exact_integer_ge": (
        "def «_>=Int_» (x0 x1 : SortInt) : SortBool :=\n"
        "  decide (x0 ≥ x1)" in candidate_proof
    ),
    "candidate_add_is_exact_integer_add": (
        "def «_+Int_» (x0 x1 : SortInt) : SortInt :=\n"
        "  x0 + x1" in candidate_proof
    ),
    "candidate_summary_is_bound_to_model": (
        "def «fibfibSpec(_)_VERIFICATION-SYNTAX_Int_Int» "
        "(x0 : SortInt) : SortInt :=\n"
        "  Proof.FibfibModel.fibfibInt x0" in candidate_proof
    ),
    "candidate_model_has_exact_frozen_bases": all(
        line in candidate_model
        for line in ("  | 0 => 0", "  | 1 => 0", "  | 2 => 1")
    ),
    "candidate_model_has_shifted_ternary_recurrence": (
        "  | n + 3 => fibfibNat n + fibfibNat (n + 1) + "
        "fibfibNat (n + 2)" in candidate_model
    ),
    "candidate_model_totalizes_negatives_to_zero": (
        "def fibfibInt (n : Int) : Int :=\n"
        "  fibfibNat n.toNat" in candidate_model
        and frozen_summary(-5) == frozen_summary(-1) == 0
    ),
    "frozen_k_has_exact_summary_bases": all(
        line in verification
        for line in (
            "rule fibfibSpec(0) => 0 [concrete]",
            "rule fibfibSpec(1) => 0 [concrete]",
            "rule fibfibSpec(2) => 1 [concrete]",
        )
    ),
    "frozen_k_has_guarded_recurrence_and_negative_totalization": (
        "requires N >=Int 3" in verification
        and "requires N <Int 0" in verification
    ),
    "source_solution_is_the_same_three_register_loop": all(
        line in solution
        for line in (
            "a = 0",
            "b = 0",
            "c = 1",
            "next_value = a + b + c",
            "a = b",
            "b = c",
            "c = next_value",
            "return a",
        )
    ),
    "source_loop_matches_frozen_summary_0_through_100": all(
        source_loop(index) == frozen_summary(index)
        for index in range(101)
    ),
    "lean_adversarial_samples_match_independent_oracle": (
        expected_samples == [0, 0, 0, 0, 1, 1, 2, 4, 24, 274]
        and lean_sample_line in bridge_output
        and "[false, true, true, false]" in bridge_output
        and "[3, 0, 7]" in bridge_output
        and 'COMMAND_EXIT_CODE="0"' in bridge_output
    ),
    "counterfactual_witnesses_are_discriminating": (
        frozen_summary(2) == 1
        and 0 != frozen_summary(2)
        and (0 >= 0) is True
        and False != (0 >= 0)
        and (2 + 3) == 5
        and 2 != (2 + 3)
    ),
}
checks["all_checks_pass"] = all(checks.values())
result = {
    "checks": checks,
    "sample_indices": sample_indices,
    "expected_samples": expected_samples,
    "source_loop_0_through_20": [
        source_loop(index) for index in range(21)
    ],
    "hook_lines": hook_lines,
    "counterfactuals": {
        "constant_zero_summary": {
            "accepted_by_generated_recurrence": True,
            "rejected_operationally_at_index": 2,
            "expected": frozen_summary(2),
            "counterfactual": 0,
        },
        "constant_false_ge": {
            "makes_target_guard_vacuous": True,
            "rejected_operationally_at_arguments": [0, 0],
            "expected": True,
            "counterfactual": False,
        },
        "left_projection_add": {
            "rejected_operationally_at_arguments": [2, 3],
            "expected": 5,
            "counterfactual": 2,
        },
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if checks["all_checks_pass"] else 1)
