#!/usr/bin/env bash
set -u

work=/tmp/audit-work/159-eat-audit/rebuild
overall=0

cd "$work" || exit 2
for claim_number in 1 2 3 4 5 6; do
  spec="spec-claim-${claim_number}.k"
  module="SPEC-CLAIM-${claim_number}"
  printf '$ kprove %s --definition proof-kompiled --spec-module %s\n' \
    "$spec" "$module"
  output="$(kprove "$spec" --definition proof-kompiled --spec-module "$module" 2>&1)"
  status=$?
  printf '%s\n' "$output"
  printf '[exit=%d]\n' "$status"
  if [[ "$status" -ne 0 || "$output" != *"#Top"* ]]; then
    overall=1
  fi
done

printf 'individual_claims=6 overall=%d\n' "$overall"
exit "$overall"
