#!/usr/bin/env bash
set -u

printf '%s\n' 'COMMAND: nl -ba /tmp/audit-work/reconstruction/solution.mpy'
nl -ba /tmp/audit-work/reconstruction/solution.mpy
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || exit 1

printf '%s\n' 'COMMAND: nl -ba /tmp/audit-work/reconstruction/verification.k'
nl -ba /tmp/audit-work/reconstruction/verification.k
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || exit 1

printf '%s\n' 'COMMAND: nl -ba /tmp/audit-work/reconstruction/spec.k'
nl -ba /tmp/audit-work/reconstruction/spec.k
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || exit 1

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/claim_accounting.py'
python3 /audit-output/evidence/claim_accounting.py
code=$?
printf 'EXIT: %s\n' "$code"
exit "$code"
