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
run_bounded "$evidence/05-totality-witness-dry-run.log" \
  kprove 05-totality-witness.k \
    --definition "$definition" \
    --spec-module TOTALITY-WITNESS \
    --dry-run \
  || exit $?

run_bounded "$evidence/05-totality-witness-proof.log" \
  kprove 05-totality-witness.k \
    --definition "$definition" \
    --spec-module TOTALITY-WITNESS \
  || exit $?

echo 'TOTALITY_FALSE_CONCLUSION_WITNESS_EXIT_STATUS: 0'
