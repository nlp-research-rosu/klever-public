#!/usr/bin/env bash
set -uo pipefail
set -x

scratch=/tmp/audit-work/forty-triples-audit
cd "$scratch/candidate-src" || exit 1

kprove spec-vacuity.k \
  --definition "$scratch/verification-kompiled" \
  --spec-module SPEC-VACUITY \
  --claims false-length-three \
  --output pretty
