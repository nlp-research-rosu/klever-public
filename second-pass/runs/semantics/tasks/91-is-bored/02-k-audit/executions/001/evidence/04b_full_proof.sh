#!/usr/bin/env bash
set -u

printf 'All five positive claims, including the mutually recursive loop circularities:\n'
printf '$ timeout 900s kprove spec.k --definition /tmp/audit-work/build/verification-kompiled --spec-module SPEC\n'
timeout 900s kprove spec.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC
status=$?
printf '[exit %d]\n' "$status"
exit "$status"
