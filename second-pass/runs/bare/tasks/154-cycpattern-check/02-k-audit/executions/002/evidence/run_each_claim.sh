#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/154-cycpattern-check
definition="$scratch/verification-haskell-kompiled"
spec="$scratch/spec-labeled.k"
evidence=/audit-output/evidence

labels=(
  example-abcd
  example-hello
  example-whassup
  example-abab
  example-efef
  example-himenss
  boundary-unrotated
  boundary-single
  boundary-empty-ground
  boundary-empty-symbolic
  loop-invariant
)

overall=0
for label in "${labels[@]}"; do
  selector="SPEC-LABELED.$label"
  log="$evidence/kprove_claim_${label}.log"
  printf 'COMMAND: kprove %q --definition %q --spec-module SPEC-LABELED --claims %q --warnings none\n' \
    "$spec" "$definition" "$selector" | tee "$log"
  kprove "$spec" \
    --definition "$definition" \
    --spec-module SPEC-LABELED \
    --claims "$selector" \
    --warnings none 2>&1 | tee -a "$log"
  status=${PIPESTATUS[0]}
  printf 'EXIT_STATUS=%s\n' "$status" | tee -a "$log"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
done

# The whole-program claim is designed to use the loop claim as its circular
# invariant, so retain that dependency while selecting this target.
selector=SPEC-LABELED.loop-invariant,SPEC-LABELED.whole-program
log="$evidence/kprove_claim_whole-program_with_invariant.log"
printf 'COMMAND: kprove %q --definition %q --spec-module SPEC-LABELED --claims %q --warnings none\n' \
  "$spec" "$definition" "$selector" | tee "$log"
kprove "$spec" \
  --definition "$definition" \
  --spec-module SPEC-LABELED \
  --claims "$selector" \
  --warnings none 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}
printf 'EXIT_STATUS=%s\n' "$status" | tee -a "$log"
if [[ "$status" -ne 0 ]]; then
  overall=1
fi

printf 'OVERALL_EXIT_STATUS=%s\n' "$overall"
exit "$overall"
