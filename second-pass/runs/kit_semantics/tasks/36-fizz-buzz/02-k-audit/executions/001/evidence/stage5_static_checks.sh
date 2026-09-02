#!/usr/bin/env bash
set +e

printf 'COMMAND: python3 /audit-output/evidence/build_rule_inventory.py\n'
python3 /audit-output/evidence/build_rule_inventory.py
status=$?
printf 'EXIT STATUS: %s\n' "$status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

printf 'COMMAND: python3 /audit-output/evidence/proof_equation_audit.py\n'
python3 /audit-output/evidence/proof_equation_audit.py
status=$?
printf 'EXIT STATUS: %s\n' "$status"
if [ "$status" -ne 0 ]; then
  exit "$status"
fi

printf 'COMMAND: rg -n no-evaluators reference-semantics/semantics/*.k verification.k spec.k\n'
rg -n no-evaluators reference-semantics/semantics/*.k verification.k spec.k
status=$?
printf 'EXIT STATUS: %s\n' "$status"
exit 0
