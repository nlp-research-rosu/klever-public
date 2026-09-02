#!/usr/bin/env bash
set -u

definition="/tmp/audit-work/19-sort-numbers/reviewer-verification-kompiled"
spec="/tmp/audit-work/19-sort-numbers/spec.k"
claims=(
  sort-numbers
  key-zero
  key-one
  key-two
  key-three
  key-four
  key-five
  key-six
  key-seven
  key-eight
  key-nine
)

overall=0
for label in "${claims[@]}"; do
  output="/audit-output/evidence/03-claim-${label}.out"
  printf 'COMMAND: kprove %q --definition %q --spec-module SPEC --claims %q\n' \
    "$spec" "$definition" "SPEC.${label}"
  kprove "$spec" \
    --definition "$definition" \
    --spec-module SPEC \
    --claims "SPEC.${label}" 2>&1 | tee "$output"
  status=${PIPESTATUS[0]}
  top_count=$(grep -c '^#Top$' "$output" || true)
  printf 'EXIT: %s; EXACT_TOP_LINES: %s; CLAIM: %s\n' "$status" "$top_count" "$label"
  if [[ "$status" -ne 0 || "$top_count" -lt 1 ]]; then
    overall=1
  fi
done

printf 'OVERALL_EXIT: %s\n' "$overall"
exit "$overall"
