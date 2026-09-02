#!/usr/bin/env bash
set -u

aggregate=0
for label in prompt-example-0 prompt-example-1; do
  printf '\n=== independently selected concrete entry claim %s ===\n' "$label"
  printf '$ timeout 300s kprove spec.k --definition /tmp/audit-work/build/verification-kompiled --spec-module SPEC --claims %q\n' "$label"
  timeout 300s kprove spec.k \
    --definition /tmp/audit-work/build/verification-kompiled \
    --spec-module SPEC \
    --claims "$label"
  status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then
    aggregate=1
  fi
done
exit "$aggregate"
