#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruction

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/04_constructor_compare.py'
python3 /audit-output/evidence/04_constructor_compare.py
compare_status=$?
printf 'EXIT: %s\n' "$compare_status"

printf '%s\n' 'COMMAND: python3 -c (import trusted canonical and candidate; print n=4 results)'
python3 -c 'import canonical, solution; print("canonical_n4=", canonical.special_factorial(4)); print("candidate_n4=", solution.special_factorial(4))'
python_status=$?
printf 'EXIT: %s\n' "$python_status"

cp /audit-output/evidence/04_witnesses.k audit-witnesses.k
printf '%s\n' 'COMMAND: kprove audit-witnesses.k --definition audit-verification-kompiled --spec-module AUDIT-WITNESSES'
kprove audit-witnesses.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-WITNESSES
witness_status=$?
printf 'EXIT: %s\n' "$witness_status"

if [ "$compare_status" -ne 0 ] || [ "$python_status" -ne 0 ] || [ "$witness_status" -ne 0 ]; then
  exit 1
fi
