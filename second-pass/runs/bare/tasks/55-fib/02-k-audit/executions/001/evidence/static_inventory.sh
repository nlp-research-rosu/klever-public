#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/src || exit 1

printf '%s\n' 'COMMAND: nl -ba semantic.k'
nl -ba semantic.k
printf '%s\n' 'COMMAND: nl -ba verification.k'
nl -ba verification.k
printf '%s\n' 'COMMAND: nl -ba spec.k'
nl -ba spec.k
printf '%s\n' 'COMMAND: rg -n syntax|configuration|rule|claim|\\[(function|functional|total|simplification|priority) semantic.k verification.k spec.k'
rg -n \
  'syntax|configuration|rule|claim|\[(function|functional|total|simplification|priority)' \
  semantic.k verification.k spec.k
