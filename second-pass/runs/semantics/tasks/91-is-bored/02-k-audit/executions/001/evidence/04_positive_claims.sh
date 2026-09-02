#!/usr/bin/env bash
set -u

run_claim() {
  label=$1
  printf '\n=== claim %s ===\n' "$label"
  printf '$ timeout 300s kprove spec.k --definition /tmp/audit-work/build/verification-kompiled --spec-module SPEC --claims %q\n' "$label"
  timeout 300s kprove spec.k \
    --definition /tmp/audit-work/build/verification-kompiled \
    --spec-module SPEC \
    --claims "$label"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

aggregate=0
for label in \
  loop-state-0 \
  loop-state-1 \
  loop-state-2 \
  prompt-example-0 \
  prompt-example-1
do
  if ! run_claim "$label"; then
    aggregate=1
  fi
done

exit "$aggregate"
