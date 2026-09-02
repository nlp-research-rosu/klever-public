#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/43-pairs-sum-to-zero
definition="$scratch/proof-kompiled"
evidence=/audit-output/evidence

run_bounded() {
  local log="$1"
  shift
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
  } > "$log"
  set -o pipefail
  "$@" 2>&1 | sed -n '1,220p' >> "$log"
  local status=${PIPESTATUS[0]}
  set +o pipefail
  echo "EXIT_STATUS: $status" >> "$log"
  return "$status"
}

cd "$scratch" || exit 91

for item in \
  '04-ground-empty.k:SPEC-GROUND-EMPTY:04-ground-empty.log' \
  '04-ground-two-zeroes.k:SPEC-GROUND-TWO-ZEROES:04-ground-two-zeroes.log' \
  '04-ground-no-pair.k:SPEC-GROUND-NO-PAIR:04-ground-no-pair.log'
do
  IFS=: read -r source module log <<< "$item"
  run_bounded "$evidence/$log" \
    kprove "$source" --definition "$definition" --spec-module "$module" \
    || exit $?
done

run_bounded "$evidence/04-body-mutation-dry-run.log" \
  kprove 04-body-mutation.k \
    --definition "$definition" \
    --spec-module SPEC-BODY-MUTATION \
    --dry-run \
  || exit $?

run_bounded "$evidence/04-body-mutation-proof.log" \
  kprove 04-body-mutation.k \
    --definition "$definition" \
    --spec-module SPEC-BODY-MUTATION
body_status=$?
if (( body_status == 0 )); then
  echo 'UNEXPECTED: body mutation proved' >&2
  exit 92
fi

echo "EXPECTED_BODY_MUTATION_PROOF_FAILURE_STATUS: $body_status"
exit 0
