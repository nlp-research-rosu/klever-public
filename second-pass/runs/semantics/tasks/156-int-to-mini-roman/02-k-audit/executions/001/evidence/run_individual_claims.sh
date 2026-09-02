#!/usr/bin/env bash
set -u

workdir=/tmp/audit-work/candidate
summary=/audit-output/evidence/stage3-individual-claims-summary.log
: > "$summary"

run_one() {
  local definition=$1
  local module=$2
  local label=$3
  local log="/audit-output/evidence/stage3-claim-${label}.log"
  local command=(
    kprove spec.k
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
  local status=$?
  printf 'EXIT: %d\n' "$status" | tee -a "$summary"
  if [[ "$status" -eq 0 ]] && rg -q '^#Top$' "$log"; then
    printf 'RESULT: #Top\n' | tee -a "$summary"
  else
    printf 'RESULT: NOT_CLOSED\n' | tee -a "$summary"
    sed -n '1,120p' "$log" | tee -a "$summary"
    return 1
  fi
}

failed=0
for label in \
  thousandsHelper \
  hundredsHelper \
  tensHelper \
  onesHelper \
  thousandsIndexRange \
  hundredsIndexRange \
  tensIndexRange \
  onesIndexRange
do
  run_one fresh-lemma-kompiled ROMAN-LEMMA-SPEC "$label" || failed=1
done
run_one fresh-verification-kompiled ROMAN-SPEC romanCorrect || failed=1

printf 'OVERALL_EXIT: %d\n' "$failed" | tee -a "$summary"
exit "$failed"
