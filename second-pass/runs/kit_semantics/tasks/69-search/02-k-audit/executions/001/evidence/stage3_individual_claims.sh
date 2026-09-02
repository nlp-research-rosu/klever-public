#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/reconstruction
status=0

names=(
  inner-loop
  outer-loop-with-inner-dependency
  search-program-with-loop-dependencies
)
filters=(
  SPEC.inner-loop
  SPEC.inner-loop,SPEC.outer-loop
  SPEC.inner-loop,SPEC.outer-loop,SPEC.search-program
)

for index in "${!names[@]}"; do
  name="${names[$index]}"
  filter="${filters[$index]}"
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims "$filter" \
    2>&1 |
    tail -n 200 |
    tee "/audit-output/evidence/stage3_kprove_${name}_bounded.log"
  claim_exit="${PIPESTATUS[0]}"
  printf 'target=%s filter=%s exit=%s\n' "$name" "$filter" "$claim_exit"
  if [[ "$claim_exit" != 0 ]] ||
     ! grep -qx '#Top' "/audit-output/evidence/stage3_kprove_${name}_bounded.log"; then
    status=1
  fi
done

printf 'stage3_individual_claims_exit=%s\n' "$status"
exit "$status"
