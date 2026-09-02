#!/usr/bin/env bash
set -uo pipefail

kprove spec-vacuity-fresh.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-FRESH \
  --dry-run
status=$?
printf 'vacuity_dry_run_exit=%s\n' "$status"
exit "$status"
