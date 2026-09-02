#!/usr/bin/env bash
set -uxo pipefail

kprove /tmp/audit-work/fresh/spec-vacuity.k \
  --definition /tmp/audit-work/fresh/proof-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.concatenate-false-empty
mutation_status=$?
printf 'MUTATION_KPROVE_EXIT_STATUS=%d\n' "$mutation_status"
test "$mutation_status" -ne 0
