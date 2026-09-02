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
  "$@" 2>&1 | sed -n '1,240p' >> "$log"
  local status=${PIPESTATUS[0]}
  set +o pipefail
  echo "EXIT_STATUS: $status" >> "$log"
  return "$status"
}

cd "$scratch" || exit 91

run_bounded "$evidence/06-vacuity-dry-run.log" \
  kprove 06-spec-vacuity.k \
    --definition "$definition" \
    --spec-module SPEC-VACUITY \
    --dry-run \
  || exit $?

run_bounded "$evidence/06-vacuity-proof.log" \
  kprove 06-spec-vacuity.k \
    --definition "$definition" \
    --spec-module SPEC-VACUITY
proof_status=$?
if (( proof_status == 0 )); then
  echo 'UNEXPECTED: false-postcondition mutation proved' >&2
  exit 92
fi

echo "EXPECTED_FALSE_POSTCONDITION_FAILURE_STATUS: $proof_status"
exit 0
