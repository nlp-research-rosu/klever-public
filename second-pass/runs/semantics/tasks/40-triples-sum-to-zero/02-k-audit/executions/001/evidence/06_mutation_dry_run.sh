#!/usr/bin/env bash
set -uo pipefail
set -x

scratch=/tmp/audit-work/forty-triples-audit
cp -a /audit-output/evidence/spec-vacuity.k \
  "$scratch/candidate-src/spec-vacuity.k"
cd "$scratch/candidate-src" || exit 1

kprove spec-vacuity.k \
  --definition "$scratch/verification-kompiled" \
  --spec-module SPEC-VACUITY \
  --claims false-length-three \
  --dry-run \
  --output none
