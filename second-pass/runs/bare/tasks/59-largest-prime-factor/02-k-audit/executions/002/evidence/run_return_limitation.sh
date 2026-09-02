#!/usr/bin/env bash
set -u

program=/tmp/audit-work/59-largest-prime-factor/source/return-followed.mpy
definition=/tmp/audit-work/59-largest-prime-factor/build-stage3-fresh/semantic-kompiled

printf '%s\n' \
  "COMMAND: krun $program --definition $definition -cN=4 --output pretty"
krun "$program" --definition "$definition" -cN=4 --output pretty
command_status=$?
printf 'EXIT: %d\n' "$command_status"
printf '%s\n' \
  'EXPECTED PYTHON: the first return terminates with value 1; the second is unreachable.'
