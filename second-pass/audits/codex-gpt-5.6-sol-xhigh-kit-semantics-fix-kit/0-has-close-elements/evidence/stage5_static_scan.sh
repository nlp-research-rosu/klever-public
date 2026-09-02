#!/usr/bin/env bash
set -u
set -x

scratch=/tmp/audit-work/reconstruction

rg -n '^\s*(syntax|rule|context|claim|configuration)\b' \
  "$scratch/verification.k" "$scratch/spec.k"
local_inventory_status=$?

rg -n '^\s*(syntax|rule|claim).*?(has_close_elements|hasClose|closeInner|closeOuter|HC-)' \
  "$scratch/reference-semantics"
task_answer_in_baseline_status=$?

rg -n '\b(simplification|functional)\b' \
  "$scratch/reference-semantics" "$scratch/verification.k" "$scratch/spec.k"
simplification_or_functional_status=$?

rg -n 'no-evaluators|symbol\(' \
  "$scratch/reference-semantics" "$scratch/verification.k"
opaque_inventory_status=$?

rg -n 'priority\(' "$scratch/verification.k"
local_priority_status=$?

rg -n -F 'applyBin("-"' \
  "$scratch/reference-semantics" "$scratch/verification.k"
minus_overlap_status=$?

rg -n -F 'applyBuiltin("abs"' \
  "$scratch/reference-semantics" "$scratch/verification.k"
abs_overlap_status=$?

rg -n -F 'applyCmp("<"' \
  "$scratch/reference-semantics" "$scratch/verification.k"
less_overlap_status=$?

printf 'LOCAL_INVENTORY_STATUS=%d\n' "$local_inventory_status"
printf 'TASK_ANSWER_IN_BASELINE_STATUS=%d (1 means no match)\n' "$task_answer_in_baseline_status"
printf 'SIMPLIFICATION_OR_FUNCTIONAL_STATUS=%d (1 means no match)\n' "$simplification_or_functional_status"
printf 'OPAQUE_INVENTORY_STATUS=%d\n' "$opaque_inventory_status"
printf 'LOCAL_PRIORITY_STATUS=%d (1 means no match)\n' "$local_priority_status"
printf 'MINUS_OVERLAP_STATUS=%d\n' "$minus_overlap_status"
printf 'ABS_OVERLAP_STATUS=%d\n' "$abs_overlap_status"
printf 'LESS_OVERLAP_STATUS=%d\n' "$less_overlap_status"

if (( local_inventory_status != 0 || opaque_inventory_status != 0 ||
      minus_overlap_status != 0 || abs_overlap_status != 0 || less_overlap_status != 0 )); then
  exit 1
fi
exit 0
