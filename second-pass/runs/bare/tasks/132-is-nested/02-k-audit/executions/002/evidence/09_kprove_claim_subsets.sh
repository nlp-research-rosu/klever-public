#!/usr/bin/env bash
set -uo pipefail

modules=(
  AUDIT-SPEC-LOOP3
  AUDIT-SPEC-LOOP2
  AUDIT-SPEC-LOOP1
  AUDIT-SPEC-LOOP0
)

overall=0
for module in "${modules[@]}"; do
  printf 'TARGET_MODULE=%s\n' "$module"
  printf 'COMMAND: kprove claim-subsets.k --definition audit-verification-kompiled --spec-module %s\n' "$module"
  kprove claim-subsets.k \
    --definition audit-verification-kompiled \
    --spec-module "$module"
  status=$?
  printf 'TARGET_EXIT=%s\n' "$status"
  if [[ $status -ne 0 ]]; then
    overall=$status
  fi
done
exit "$overall"
