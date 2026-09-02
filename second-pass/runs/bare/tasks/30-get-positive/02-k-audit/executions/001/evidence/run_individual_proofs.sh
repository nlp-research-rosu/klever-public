#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/30-get-positive
proof_file="$scratch/spec-audit-labeled.k"
definition="$scratch/proof-kompiled"

targets=(
  "AUDIT-VERIFICATION helper-positive-head"
  "AUDIT-VERIFICATION helper-nonpositive-head"
  "AUDIT-VERIFICATION helper-empty"
  "AUDIT-SPEC spec-universal"
  "AUDIT-SPEC spec-example-1"
  "AUDIT-SPEC spec-example-2"
  "AUDIT-SPEC spec-empty"
  "AUDIT-SPEC spec-all-nonpositive"
)

failures=0
for target in "${targets[@]}"; do
  read -r module label <<< "$target"
  command=(
    /usr/bin/kprove
    "$proof_file"
    --definition "$definition"
    --spec-module "$module"
    --claims "$module.label($label)"
  )
  printf 'COMMAND:'
  printf ' %q' "${command[@]}"
  printf '\n'
  "${command[@]}"
  status=$?
  printf 'CLAIM_RESULT module=%s label=%s exit=%d\n' "$module" "$label" "$status"
  if [[ "$status" -ne 0 ]]; then
    failures=$((failures + 1))
  fi
done

printf 'SUMMARY targets=%d failures=%d\n' "${#targets[@]}" "$failures"
exit "$failures"
