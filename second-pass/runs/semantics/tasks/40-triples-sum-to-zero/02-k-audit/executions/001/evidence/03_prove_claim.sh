#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -ne 1 ]]; then
  echo "usage: 03_prove_claim.sh LABEL" >&2
  exit 64
fi

scratch=/tmp/audit-work/forty-triples-audit
label=$1
cd "$scratch/candidate-src" || exit 1

kprove spec.k \
  --definition "$scratch/verification-kompiled" \
  --spec-module SPEC \
  --claims "$label" \
  --output pretty
