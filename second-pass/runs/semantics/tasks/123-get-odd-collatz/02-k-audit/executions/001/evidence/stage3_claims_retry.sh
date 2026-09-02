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

printf 'Stage 3 per-claim rerun with unqualified labels\n'
for label in odd-step even-step exit-step case-1 case-5 case-6 case-7; do
  (
    cd "$src" || exit 125
    run_log "$evidence/stage3_kprove_${label}_unqualified.log" \
      kprove spec.k \
        --definition verification-kompiled-audit \
        --spec-module SPEC \
        --claims "$label" \
        --depth 2000 \
        --smt-timeout 5000
  )
done
