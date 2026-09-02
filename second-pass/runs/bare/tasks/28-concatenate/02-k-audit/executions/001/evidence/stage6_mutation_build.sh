#!/usr/bin/env bash
set -euxo pipefail

cmp /tmp/audit-work/fresh/spec-vacuity.k /audit-output/evidence/spec-vacuity.k
kprove /tmp/audit-work/fresh/spec-vacuity.k \
  --definition /tmp/audit-work/fresh/proof-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.concatenate-false-empty \
  --dry-run
