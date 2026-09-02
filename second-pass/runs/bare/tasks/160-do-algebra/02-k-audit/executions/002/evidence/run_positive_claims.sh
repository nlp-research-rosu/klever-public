#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/160-do-algebra/candidate
definition=/tmp/audit-work/160-do-algebra/proof-kompiled
spec=audit-labeled-spec.k
labels=(entry example right-pow floor-precedence mul-precedence left-sub)
overall=0

cd "$work" || exit 125
for label in "${labels[@]}"; do
  command=(
    kprove "$spec"
    --definition "$definition"
    --spec-module AUDIT-LABELED-SPEC
    --claims "AUDIT-LABELED-SPEC.$label"
  )
  printf 'COMMAND:'
  printf ' %q' "${command[@]}"
  printf '\n'
  "${command[@]}"
  status=$?
  printf 'EXIT: %d\n' "$status"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
done

exit "$overall"
