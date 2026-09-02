#!/usr/bin/env bash
set -u

workdir=/tmp/audit-work/candidate
spec=/audit-output/evidence/bridge_rule_witnesses.k
definition=fresh-lemma-kompiled
module=BASE-FALSE-WITNESSES
summary=/audit-output/evidence/stage5-base-false-summary.log
: > "$summary"
unexpected=0

for label in \
  thousandsBaseRejectsFalse \
  hundredsBaseRejectsFalse \
  tensBaseRejectsFalse \
  onesBaseRejectsFalse
do
  log="/audit-output/evidence/stage5-base-false-${label}.log"
  command=(
    kprove "$spec"
    --definition "$definition"
    --spec-module "$module"
    --claims "$module.$label"
  )
  {
    printf 'COMMAND:'
    printf ' %q' "${command[@]}"
    printf '\n'
  } | tee -a "$summary"
  (
    cd "$workdir" || exit 125
    "${command[@]}"
  ) > "$log" 2>&1
  status=$?
  printf 'EXIT: %d\n' "$status" | tee -a "$summary"
  if [[ "$status" -ne 0 ]] && rg -q 'WarnStuckClaimState' "$log"; then
    printf 'RESULT: EXPECTED_UNMET_RESULT_OBLIGATION\n' | tee -a "$summary"
    rg -n -m 1 'WarnStuckClaimState|Could not prove|backend terminated' "$log" \
      | tee -a "$summary"
  else
    printf 'RESULT: UNEXPECTED\n' | tee -a "$summary"
    sed -n '1,160p' "$log" | tee -a "$summary"
    unexpected=1
  fi
done

printf 'OVERALL_EXIT: %d\n' "$unexpected" | tee -a "$summary"
exit "$unexpected"
