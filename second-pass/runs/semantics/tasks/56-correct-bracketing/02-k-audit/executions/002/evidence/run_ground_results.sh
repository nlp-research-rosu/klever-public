#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
{
  printf 'WORKDIR: %s\n' "$work"
  printf 'COMMAND: timeout 120s kprove ground-result-spec.k --definition audit-verification-kompiled --spec-module GROUND-RESULT-SPEC --claims %q --output pretty\n' \
    'GROUND-RESULT-SPEC.empty,GROUND-RESULT-SPEC.single-open,GROUND-RESULT-SPEC.one-pair,GROUND-RESULT-SPEC.bad-prefix'
  (
    cd "$work"
    timeout 120s kprove ground-result-spec.k \
      --definition audit-verification-kompiled \
      --spec-module GROUND-RESULT-SPEC \
      --claims GROUND-RESULT-SPEC.empty,GROUND-RESULT-SPEC.single-open,GROUND-RESULT-SPEC.one-pair,GROUND-RESULT-SPEC.bad-prefix \
      --output pretty
  )
  proof_status=$?
  printf 'KPROVE_EXIT_STATUS: %d\n' "$proof_status"
  printf 'COMMAND: python3 %q\n' /audit-output/evidence/claim_witnesses.py
  python3 /audit-output/evidence/claim_witnesses.py
  python_status=$?
  printf 'PYTHON_EXIT_STATUS: %d\n' "$python_status"
} > /audit-output/evidence/stage4_ground_results.log 2>&1
