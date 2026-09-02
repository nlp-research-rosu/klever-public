#!/usr/bin/env bash
set -u
set -o pipefail

EVIDENCE=/audit-output/evidence
SCRATCH=/tmp/audit-work/reconstruction

printf '$ cp /audit-output/evidence/spec-vacuity.k /tmp/audit-work/reconstruction/spec-vacuity.k\n'
cp "$EVIDENCE/spec-vacuity.k" "$SCRATCH/spec-vacuity.k"
status=$?
printf '[exit %d]\n' "$status"

printf '$ kprove /tmp/audit-work/reconstruction/spec-vacuity.k --definition /tmp/audit-work/reconstruction/loop-lemmas-kompiled --spec-module SPEC-VACUITY --claims false-ground-result --dry-run\n'
kprove "$SCRATCH/spec-vacuity.k" \
  --definition "$SCRATCH/loop-lemmas-kompiled" \
  --spec-module SPEC-VACUITY \
  --claims false-ground-result \
  --dry-run 2>&1 | tee "$EVIDENCE/stage6_mutation_dry_run.log"
status=${PIPESTATUS[0]}
printf '[exit %d]\n' "$status"

printf '$ kprove /tmp/audit-work/reconstruction/spec-vacuity.k --definition /tmp/audit-work/reconstruction/loop-lemmas-kompiled --spec-module SPEC-VACUITY --claims false-ground-result --output pretty\n'
kprove "$SCRATCH/spec-vacuity.k" \
  --definition "$SCRATCH/loop-lemmas-kompiled" \
  --spec-module SPEC-VACUITY \
  --claims false-ground-result \
  --output pretty 2>&1 | tee "$EVIDENCE/stage6_mutation_proof.log"
status=${PIPESTATUS[0]}
printf '[exit %d]\n' "$status"
