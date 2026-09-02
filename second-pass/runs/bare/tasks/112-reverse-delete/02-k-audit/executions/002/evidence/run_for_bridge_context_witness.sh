#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/112-reverse-delete
program="$scratch/for_bridge_context_witness.mpy"
definition="$scratch/audit-semantic-llvm-kompiled"

printf '%s\n' 'PYTHON ORACLE'
python3 /audit-output/evidence/for_bridge_context_oracle.py
printf '%s\n' 'K EXECUTION'
printf 'COMMAND: krun %q --definition %q -cS=%q -cC=%q\n' \
  "$program" "$definition" '"a"' '""'
output=$(krun "$program" --definition "$definition" -cS='"a"' -cC='""')
status=$?
printf 'KRUN-EXIT: %d\n%s\n' "$status" "$output"
if (( status == 0 )) && grep -Fq 'strVal ( "OLD" )' <<<"$output"; then
  printf '%s\n' \
    'WITNESS-CONFIRMED: Python returns "a"; generated semantics returns "OLD".'
  exit 0
fi
printf '%s\n' 'WITNESS-NOT-CONFIRMED'
exit 1
