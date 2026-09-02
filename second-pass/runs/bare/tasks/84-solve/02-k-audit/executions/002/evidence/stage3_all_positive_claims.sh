#!/usr/bin/env bash
set -uo pipefail
export PATH="/root/.nix-profile/bin:$PATH"

work=/tmp/audit-work/84-solve
definition="$work/verification-kompiled"
evidence=/audit-output/evidence
status=0
claims=(
  SPEC.inputs-00000-00999
  SPEC.inputs-01000-01999
  SPEC.inputs-02000-02999
  SPEC.inputs-03000-03999
  SPEC.inputs-04000-04999
  SPEC.inputs-05000-05999
  SPEC.inputs-06000-06999
  SPEC.inputs-07000-07999
  SPEC.inputs-08000-08999
  SPEC.inputs-09000-09999
  SPEC.input-10000
)

for claim in "${claims[@]}"; do
  safe_name=${claim//./_}
  log="$evidence/stage3_kprove_${safe_name}.log"
  printf 'COMMAND kprove %s --definition %s --spec-module SPEC --claims %s\n' \
    "$work/spec.k" "$definition" "$claim"
  kprove "$work/spec.k" \
    --definition "$definition" \
    --spec-module SPEC \
    --claims "$claim" \
    2>&1 | tee "$log"
  proof_exit=${PIPESTATUS[0]}
  if grep -qx '#Top' "$log"; then
    top_count=$(grep -xc '#Top' "$log")
  else
    top_count=0
  fi
  printf 'CLAIM %s EXIT %d TOP_COUNT %d\n' \
    "$claim" "$proof_exit" "$top_count"
  printf 'COMMAND_EXIT %d\n' "$proof_exit" >> "$log"
  printf 'TOP_COUNT %d\n' "$top_count" >> "$log"
  if [[ "$proof_exit" -ne 0 || "$top_count" -lt 1 ]]; then
    status=1
  fi
done

printf 'CLAIM_COUNT %d\n' "${#claims[@]}"
printf 'OVERALL_EXIT %d\n' "$status"
exit "$status"
