#!/usr/bin/env bash
set -uo pipefail

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
proof_status=$?
printf 'kprove_exit=%s\n' "$proof_status"
exit "$proof_status"
