#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/candidate
definition=/tmp/audit-work/runs/verification-kompiled
false_spec="$scratch/audit-false-postcondition.k"

echo "COMMAND[witness]: python3 /audit-output/evidence/05_mutation_witness.py"
python3 /audit-output/evidence/05_mutation_witness.py
witness_status=$?
echo "EXIT[witness]: $witness_status"

echo "COMMAND[dry-run]: kprove $false_spec --definition $definition --spec-module AUDIT-FALSE-POSTCONDITION --dry-run"
kprove "$false_spec" \
  --definition "$definition" \
  --spec-module AUDIT-FALSE-POSTCONDITION \
  --dry-run
dry_status=$?
echo "EXIT[dry-run]: $dry_status"

echo "COMMAND[false-proof]: kprove $false_spec --definition $definition --spec-module AUDIT-FALSE-POSTCONDITION"
kprove "$false_spec" \
  --definition "$definition" \
  --spec-module AUDIT-FALSE-POSTCONDITION
proof_status=$?
echo "EXIT[false-proof]: $proof_status"

if [[ "$witness_status" -eq 0 && "$dry_status" -eq 0 && "$proof_status" -eq 1 ]]; then
  echo "FRESH_NONVACUITY=PASS"
  exit 0
fi
echo "FRESH_NONVACUITY=FAIL"
exit 1
