#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

cd /tmp/audit-work/candidate
kprove spec.k \
  --definition auditor-verification-kompiled \
  --spec-module SPEC
status=$?
printf 'complete_spec_kprove_exit=%s\n' "$status"
exit "$status"
