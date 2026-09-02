#!/usr/bin/env bash
set -uo pipefail

source_dir=/tmp/audit-work/94-skjkasdkd/source
definition=/tmp/audit-work/94-skjkasdkd/build/verification-kompiled
status=0

for expression in 'refPrimeFrom(5, 2)' 'refPrimeFrom(4, 2)' 'refPrimeFrom(5, 0)'; do
  slug=$(printf '%s' "$expression" | tr -cd '[:alnum:]')
  term="$source_dir/$slug.kore"
  echo "EXPRESSION: $expression"
  echo "KAST_COMMAND: kast --expression $expression --definition $definition --module VERIFICATION --sort Bool --output kore"
  kast \
    --expression "$expression" \
    --definition "$definition" \
    --module VERIFICATION \
    --sort Bool \
    --output kore > "$term"
  kast_status=$?
  echo "KAST_EXIT: $kast_status"
  echo "KRUN_COMMAND: krun $term --term --parser cat --definition $definition"
  krun "$term" --term --parser cat --definition "$definition"
  krun_status=$?
  echo "KRUN_EXIT: $krun_status"
  if [[ "$kast_status" -ne 0 || "$krun_status" -ne 0 ]]; then
    status=1
  fi
  echo "---"
done

exit "$status"
