#!/usr/bin/env bash
set -u

cd /tmp/audit-work/review/candidate-src
printf 'PWD=%s\n' "$PWD"
printf '%s\n' \
  'COMMAND: kprove spec.k --definition audit-verification-kompiled --spec-module SPEC'
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
status=$?
printf 'KPROVE_ALL_EXIT=%s\n' "$status"
exit "$status"
