#!/usr/bin/env bash
set -u

printf 'Mutually recursive loop claims selected as their minimal proof unit:\n'
printf '$ timeout 600s kprove spec.k --definition /tmp/audit-work/build/verification-kompiled --spec-module SPEC --claims loop-state-0,loop-state-1,loop-state-2\n'
timeout 600s kprove spec.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC \
  --claims loop-state-0,loop-state-1,loop-state-2
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
