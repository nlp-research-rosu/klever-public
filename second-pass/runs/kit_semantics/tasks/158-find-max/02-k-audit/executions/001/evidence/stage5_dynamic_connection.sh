#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruct-001
evidence=/audit-output/evidence
status=0

run_logged() {
  name=$1
  shift
  log=$evidence/"$name".log
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@" > "$log" 2>&1
  rc=$?
  printf '%s exit=%d log=%s\n' "$name" "$rc" "$log"
  if (( rc != 0 )); then
    status=1
  fi
}

cd "$evidence" || exit 2
run_logged \
  stage5_kompile_dynamic_connection \
  kompile --backend haskell audit-dynamic-connection.k \
    --main-module AUDIT-DYNAMIC-CONNECTION \
    --syntax-module MPY-SYNTAX \
    --output-definition "$scratch/audit-dynamic-connection-kompiled"

run_logged \
  stage5_kprove_dynamic_connection \
  kprove audit-dynamic-connection-spec.k \
    --definition "$scratch/audit-dynamic-connection-kompiled" \
    --spec-module AUDIT-DYNAMIC-CONNECTION-SPEC

printf 'overall=%d\n' "$status"
exit "$status"
