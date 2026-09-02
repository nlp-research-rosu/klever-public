#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/source
kprove unsound-apply-int-witness.k \
  --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module UNSOUND-APPLY-INT-WITNESS 2>&1 \
  | tee /tmp/audit-work/unsound-apply-int-witness.out
rg -q '#Top' /tmp/audit-work/unsound-apply-int-witness.out
python3 -c 'from solution import truncate_number; result = truncate_number(2.0); print("REAL_PROGRAM_INPUT=2.0 REAL_PROGRAM_RESULT=", result); assert result == 0.0'
echo "UNSOUND_APPLY_INT_FALSE_CONCLUSION_WITNESS_CONFIRMED"
