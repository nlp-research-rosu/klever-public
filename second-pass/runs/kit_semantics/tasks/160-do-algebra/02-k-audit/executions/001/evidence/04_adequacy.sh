#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/160-do-algebra
definition="$scratch/audit-verification-kompiled"

echo "COMMAND: python3 /audit-output/evidence/04_pinning.py"
python3 /audit-output/evidence/04_pinning.py
pin_status=$?
echo "PINNING_EXIT_STATUS=$pin_status"
if (( pin_status != 0 )); then
  exit "$pin_status"
fi

cp /audit-output/evidence/04_witness.k "$scratch/04_witness.k"
echo "COMMAND: kprove 04_witness.k --definition audit-verification-kompiled --spec-module AUDIT-WITNESS"
(
  cd "$scratch" || exit 90
  kprove 04_witness.k \
    --definition audit-verification-kompiled \
    --spec-module AUDIT-WITNESS
)
witness_status=$?
echo "WITNESS_EXIT_STATUS=$witness_status"
exit "$witness_status"
