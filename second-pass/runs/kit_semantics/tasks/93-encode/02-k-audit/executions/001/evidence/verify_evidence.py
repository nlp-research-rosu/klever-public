#!/usr/bin/env python3
"""Final consistency check over the reviewer-authored bounded evidence set."""

from __future__ import annotations

from pathlib import Path


root = Path("/audit-output/evidence")


def text(name: str) -> str:
    return (root / name).read_text(encoding="utf-8")


success_logs = [
    "01b-provenance-and-generation-records.log",
    "02-translation-identity.log",
    "03-independent-differential.log",
    "04-concrete-build.log",
    "05-concrete-execution.log",
    "06-proof-build.log",
    "07-positive-proof.log",
    "08c-program-term-pinning-normalized.log",
    "09b-claim-ground-witnesses.log",
    "10b-exhaustive-rule-inventory.log",
    "11-mutation-construction.log",
    "13-false-mutation-build.log",
    "15b-used-construct-rule-map.log",
]
for name in success_logs:
    assert "EXIT_STATUS: 0" in text(name), name

positive = text("07-positive-proof.log")
assert positive.splitlines().count("#Top") == 1
assert "COMMAND: kprove spec.k --definition verification-kompiled-audit --spec-module SPEC" in positive

body = text("12-body-sensitivity-proof.log")
assert "EXIT_STATUS: 1" in body
assert "WarnStuckClaimState" in body
assert "79 , 81" in body and "79 , 82" in body
assert "configuration cannot be" in body

false_result = text("14-false-mutation-proof.log")
assert "EXIT_STATUS: 1" in false_result
assert "WarnStuckClaimState" in false_result
assert "85 , 87" in false_result and "85 , 88" in false_result
assert "configuration cannot be" in false_result

assert "TOTAL checked=3256 mismatches=0" in text("03-independent-differential.log")
assert "constructor_level_cmp_status=0" in text("08c-program-term-pinning-normalized.log")
assert "false_mutation_witness input='u' correct='W' mutated='X'" in text(
    "09b-claim-ground-witnesses.log"
)
assert "opaque_symbols_in_solution_or_spec=[]" in text("15b-used-construct-rule-map.log")
assert "verification_local_rules=0" in text("15b-used-construct-rule-map.log")

for name in ["spec-body-audit.k", "spec-false-audit.k"]:
    assert (root / name).is_file() and (root / name).stat().st_size > 0

print(f"successful_logs_checked={len(success_logs)}")
print("positive_proof_top_count=1")
print("body_sensitivity_expected_stuck=True")
print("false_result_expected_stuck=True")
print("EVIDENCE_CONSISTENCY=PASS")
