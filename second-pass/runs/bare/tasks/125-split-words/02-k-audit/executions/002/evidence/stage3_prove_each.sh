#!/usr/bin/env bash
set -uo pipefail

definition=/tmp/audit-work/candidate/proof-kompiled
spec=/audit-output/evidence/audit-positive-specs.k
modules=(
  AUDIT-SPEC-UNIVERSAL
  AUDIT-SPEC-SPACE-EXAMPLE
  AUDIT-SPEC-COMMA-EXAMPLE
  AUDIT-SPEC-COUNT-EXAMPLE
  AUDIT-SPEC-EMPTY
  AUDIT-SPEC-PRECEDENCE
  AUDIT-SPEC-UNICODE-WHITESPACE
  AUDIT-SPEC-REPEATED-COMMA
)

overall=0
for module in "${modules[@]}"; do
  echo "COMMAND: kprove $spec --definition $definition --spec-module $module"
  kprove "$spec" --definition "$definition" --spec-module "$module"
  status=$?
  echo "EXIT_STATUS: $status"
  if (( status != 0 )); then
    overall=1
  fi
done
exit "$overall"
