#!/usr/bin/env bash
set -uo pipefail

source_dir=/tmp/audit-work/118-get-closest-vowel/candidate-src
definition=/tmp/audit-work/118-get-closest-vowel/build/proof-kompiled
overall=0

cd "$source_dir" || exit 99
for number in $(seq -w 1 13); do
  label="SPEC.claim-$number"
  printf 'COMMAND=kprove spec-audit.k --definition %q --spec-module SPEC --claims %q --warnings none\n' \
    "$definition" "$label"
  kprove spec-audit.k \
    --definition "$definition" \
    --spec-module SPEC \
    --claims "$label" \
    --warnings none
  status=$?
  printf 'CLAIM=%s EXIT_STATUS=%s\n' "$label" "$status"
  if (( status != 0 )); then
    overall=1
  fi
done
printf 'OVERALL_EXIT_STATUS=%s\n' "$overall"
exit "$overall"
