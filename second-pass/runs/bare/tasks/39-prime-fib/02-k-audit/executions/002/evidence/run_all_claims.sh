#!/usr/bin/env bash
set -uo pipefail

work="/tmp/audit-work/39-prime-fib/src"
cd "$work" || exit 1

overall=0

for label in concrete-1 concrete-2 concrete-3 concrete-4 concrete-5; do
  command=(
    kprove concrete-spec.k
    --definition audit-concrete-kompiled
    --spec-module CONCRETE-SPEC
    --claims "CONCRETE-SPEC.${label}"
    --color off
  )
  printf 'CLAIM_COMMAND:'
  printf ' %q' "${command[@]}"
  printf '\n'
  "${command[@]}"
  status=$?
  printf 'CLAIM_EXIT %s: %s\n' "$label" "$status"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
done

for label in prime-fib-correct example-1 example-2 example-3 example-4 example-5; do
  command=(
    kprove spec.k
    --definition audit-verification-kompiled
    --spec-module SPEC
    --claims "SPEC.${label}"
    --color off
  )
  printf 'CLAIM_COMMAND:'
  printf ' %q' "${command[@]}"
  printf '\n'
  "${command[@]}"
  status=$?
  printf 'CLAIM_EXIT %s: %s\n' "$label" "$status"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
done

exit "$overall"
