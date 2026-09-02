#!/usr/bin/env bash
set -uo pipefail

kprove pin-check.k \
  --definition audit-verification-kompiled \
  --spec-module PIN-CHECK
status=$?
printf 'pin_check_kprove_exit=%s\n' "$status"
exit "$status"
