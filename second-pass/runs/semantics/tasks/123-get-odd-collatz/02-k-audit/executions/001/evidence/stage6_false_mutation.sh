#!/usr/bin/env bash
set -u
set -o pipefail

src=/tmp/audit-work/123-get-odd-collatz/proof-src
evidence=/audit-output/evidence

run_log() {
  local log_file=$1
  shift
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local command_rc=$?
    printf '[exit %d]\n' "$command_rc"
    return "$command_rc"
  } 2>&1 | tee "$log_file"
  local pipeline_rc=${PIPESTATUS[0]}
  printf '[recorded exit %d in %s]\n' "$pipeline_rc" "$log_file"
  return 0
}

printf 'Stage 6 fresh false-result mutation\n'
printf 'Satisfying witness: initial input 5; Python expected result [1, 5].\n'
printf 'Mutation: retain the real trace object [5, 1] but require the returned list object to be sortVS([7, 1]).\n'

(
  cd "$src" || exit 125
  run_log "$evidence/stage6_mutation_dry_run.log" \
    kprove spec-vacuity-audit.k \
      --definition verification-kompiled-audit \
      --spec-module SPEC-VACUITY-AUDIT \
      --dry-run
)

(
  cd "$src" || exit 125
  run_log "$evidence/stage6_mutation_proof.log" \
    kprove spec-vacuity-audit.k \
      --definition verification-kompiled-audit \
      --spec-module SPEC-VACUITY-AUDIT \
      --depth 2000 \
      --smt-timeout 5000
)
