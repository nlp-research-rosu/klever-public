#!/usr/bin/env bash
set -euo pipefail

definition=/tmp/audit-work/104-unique-digits/candidate/verification-audit-kompiled
spec=/audit-output/evidence/spec_labeled.k

for claim in entry odd-true odd-false example-one example-two; do
  log_label="stage3_claim_${claim//-/_}"
  /audit-output/evidence/run_logged.sh "$log_label" \
    kprove "$spec" \
      --definition "$definition" \
      --spec-module SPEC-LABELED \
      --claims "SPEC-LABELED.$claim"
done
