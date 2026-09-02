#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/87-get-row
spec="$scratch/source/spec-labeled.k"
definition="$scratch/verification-audit-kompiled"
status=0

labels=(
  example-prompt
  example-empty
  example-third
  symbolic-000
  symbolic-001
  symbolic-010
  symbolic-011
  symbolic-100
  symbolic-101
  symbolic-110
  symbolic-111
)

for label in "${labels[@]}"; do
  printf '\nCLAIM=%s\n' "$label"
  printf '$ kprove spec-labeled.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.%s\n' "$label"
  output="$(
    kprove "$spec" \
      --definition "$definition" \
      --spec-module SPEC \
      --claims "SPEC.$label" 2>&1
  )"
  rc=$?
  printf '%s\n' "$output"
  printf 'exit=%d\n' "$rc"
  top_count="$(printf '%s\n' "$output" | grep -c '^#Top$')"
  printf 'top_line_count=%s\n' "$top_count"
  if (( rc != 0 )) || (( top_count != 1 )); then
    status=1
  fi
done

printf '\n%s\n' '$ kprove original spec.k as submitted, all claims together'
output="$(
  kprove "$scratch/source/spec.k" \
    --definition "$definition" \
    --spec-module SPEC 2>&1
)"
rc=$?
printf '%s\n' "$output"
printf 'all_claims_exit=%d\n' "$rc"
top_count="$(printf '%s\n' "$output" | grep -c '^#Top$')"
printf 'all_claims_top_line_count=%s\n' "$top_count"
if (( rc != 0 )) || (( top_count != 1 )); then
  status=1
fi

printf 'overall_exit=%d\n' "$status"
exit "$status"
