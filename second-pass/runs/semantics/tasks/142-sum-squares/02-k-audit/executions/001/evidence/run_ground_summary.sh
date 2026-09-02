#!/usr/bin/env bash
set -u

overall=0
for label in empty example-positive example-negative branch-boundaries; do
  printf '\nCOMMAND: kprove /audit-output/evidence/ground-summary.k --definition audit-verification-kompiled --spec-module GROUND-SUMMARY --claims GROUND-SUMMARY.%s --output pretty\n' "$label"
  kprove /audit-output/evidence/ground-summary.k \
    --definition audit-verification-kompiled \
    --spec-module GROUND-SUMMARY \
    --claims "GROUND-SUMMARY.$label" \
    --output pretty
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  if (( status != 0 )); then overall=1; fi
done
printf '\nOVERALL_EXIT_STATUS: %s\n' "$overall"
exit "$overall"
