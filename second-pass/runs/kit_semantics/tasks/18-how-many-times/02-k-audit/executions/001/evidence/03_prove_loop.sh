#!/usr/bin/env bash
set -u

cd /tmp/audit-work/review/candidate-src
printf 'PWD=%s\n' "$PWD"
printf '%s\n' \
  'COMMAND: kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims SPEC.loop-inv'
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-inv
status=$?
printf 'KPROVE_LOOP_EXIT=%s\n' "$status"
exit "$status"
