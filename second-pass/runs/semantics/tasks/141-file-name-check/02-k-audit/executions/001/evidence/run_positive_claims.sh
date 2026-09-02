#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/141-file-name-check
labels=(
  audit-reject-dot-count
  audit-reject-short
  audit-reject-first
  audit-reject-suffix
  audit-reject-digits
  audit-accept
)

run_one() {
  local label=$1
  local log="/audit-output/evidence/positive_${label}.log"
  {
    printf '$ kprove spec-labeled.k --definition verification-kompiled'
    printf ' --spec-module SPEC-LABELED --claims SPEC-LABELED.%s\n' "$label"
    cd "$work" || exit 125
    kprove spec-labeled.k \
      --definition verification-kompiled \
      --spec-module SPEC-LABELED \
      --claims "SPEC-LABELED.$label"
    status=$?
    printf '[exit %d]\n' "$status"
    exit "$status"
  } >"$log" 2>&1
}

pids=()
for label in "${labels[@]}"; do
  run_one "$label" &
  pids+=("$!")
done

overall=0
for index in "${!labels[@]}"; do
  if wait "${pids[$index]}"; then
    status=0
  else
    status=$?
    overall=1
  fi
  printf '%s exit=%d log=/audit-output/evidence/positive_%s.log\n' \
    "${labels[$index]}" "$status" "${labels[$index]}"
done

exit "$overall"
