#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/reconstruction
python3 /audit-output/evidence/04_pinning_and_witness.py
kprove spec-ground.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC-GROUND \
  > /audit-output/evidence/04-kprove-ground.log 2>&1
ground_status=$?
printf 'kprove_ground_exit=%s\n' "${ground_status}"
rg -n '^#Top$|WarnStuckClaimState|\\[Error\\]' \
  /audit-output/evidence/04-kprove-ground.log
