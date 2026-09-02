#!/usr/bin/env bash
set -u
set -o pipefail

exec > >(tee /audit-output/evidence/stage3-positive-proof.log) 2>&1
set -x

cd /tmp/audit-work/reconstruction || exit 90

kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC
proof_status=$?
printf 'fresh_positive_kprove_exit=%d\n' "$proof_status"

exit "$proof_status"
