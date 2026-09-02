#!/usr/bin/env bash
set -u

work=/tmp/audit-work/7-filter-by-substring/candidate
log=/audit-output/evidence/05_bridge_enabled_proof.log

printf '$ kprove spec-bridge-enabled-check.k --definition audit-verification-kompiled --spec-module FILTER-BRIDGE-ENABLED-CHECK --output pretty\n'
(
  cd "$work" || exit 125
  kprove spec-bridge-enabled-check.k \
    --definition audit-verification-kompiled \
    --spec-module FILTER-BRIDGE-ENABLED-CHECK \
    --output pretty
) >"$log" 2>&1
status=$?
printf 'EXIT: %d\n' "$status"
printf 'LOG: %s (%d lines)\n' "$log" "$(wc -l <"$log")"
sed -n '1,180p' "$log"
exit "$status"
