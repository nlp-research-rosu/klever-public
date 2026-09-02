#!/usr/bin/env bash
set -u

cd /tmp/audit-work/68-pluck || exit 90
log=/audit-output/evidence/07-kprove-all.log
{
  printf 'CWD: %s\n' "$PWD"
  printf '%s\n' 'COMMAND: kprove spec.k --definition audit-verification-kompiled --spec-module SPEC'
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  exit "$status"
} >"$log" 2>&1
