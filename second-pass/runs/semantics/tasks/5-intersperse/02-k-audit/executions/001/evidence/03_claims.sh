#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

SCRATCH=/tmp/audit-work/candidate
run cp /audit-output/evidence/03_spec_labeled.k "$SCRATCH/audit-spec-labeled.k"
run kprove "$SCRATCH/audit-spec-labeled.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module AUDIT-SPEC-LABELED
run kprove "$SCRATCH/audit-spec-labeled.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module AUDIT-SPEC-LABELED \
  --claims AUDIT-SPEC-LABELED.loop-empty
run kprove "$SCRATCH/audit-spec-labeled.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module AUDIT-SPEC-LABELED \
  --claims AUDIT-SPEC-LABELED.loop-first
run kprove "$SCRATCH/audit-spec-labeled.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module AUDIT-SPEC-LABELED \
  --claims AUDIT-SPEC-LABELED.loop-rest
run kprove "$SCRATCH/audit-spec-labeled.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module AUDIT-SPEC-LABELED \
  --claims AUDIT-SPEC-LABELED.entry
