#!/usr/bin/env bash
set -uo pipefail

proof_dir=/tmp/audit-work/reconstruction
evidence_dir=/audit-output/evidence
labels=(
  empty-input
  all-single-grades
  loop-step-new-variable
  loop-step-existing-variable
  loop-empty
  prompt-example
)

overall=0
for label in "${labels[@]}"; do
  log="$evidence_dir/stage3-kprove-${label}.log"
  (
    cd "$proof_dir" || exit 98
    printf 'COMMAND: kprove spec.k --definition verification-kompiled --spec-module SPEC --claims SPEC.%s\n' "$label"
    kprove spec.k \
      --definition verification-kompiled \
      --spec-module SPEC \
      --claims "SPEC.$label"
    rc=$?
    printf 'EXIT_STATUS: %d\n' "$rc"
    exit "$rc"
  ) 2>&1 | tee "$log"
  rc=${PIPESTATUS[0]}
  if [[ "$rc" -ne 0 ]] || ! grep -qx '#Top' "$log"; then
    printf 'CLAIM_CHECK: FAIL label=%s exit=%d top=%s\n' \
      "$label" "$rc" "$(grep -cx '#Top' "$log" || true)"
    overall=1
  else
    printf 'CLAIM_CHECK: PASS label=%s exit=0 top=1\n' "$label"
  fi
done

printf 'ALL_POSITIVE_CLAIMS_EXIT_STATUS: %d\n' "$overall"
exit "$overall"
