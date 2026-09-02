#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction || exit 90

echo "COMMAND kprove spec.k --definition verification-kompiled --spec-module MEDIAN-SPEC --claims MEDIAN-SPEC.median-odd"
kprove spec.k \
  --definition verification-kompiled \
  --spec-module MEDIAN-SPEC \
  --claims MEDIAN-SPEC.median-odd
odd_status=$?
echo "ODD_KPROVE_EXIT=$odd_status"

echo "COMMAND kprove spec.k --definition verification-kompiled --spec-module MEDIAN-SPEC --claims MEDIAN-SPEC.median-even"
kprove spec.k \
  --definition verification-kompiled \
  --spec-module MEDIAN-SPEC \
  --claims MEDIAN-SPEC.median-even
even_status=$?
echo "EVEN_KPROVE_EXIT=$even_status"

echo "SUMMARY odd=$odd_status even=$even_status"
if [[ $odd_status -eq 0 && $even_status -eq 0 ]]; then
  exit 0
fi
exit 1
