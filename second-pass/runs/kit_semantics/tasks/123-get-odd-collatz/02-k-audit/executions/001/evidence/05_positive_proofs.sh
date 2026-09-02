#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

cd /tmp/audit-work/candidate

kprove spec.k \
  --definition auditor-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.collatz-loop
loop_exit=$?
printf 'collatz_loop_kprove_exit=%s\n' "$loop_exit"

kprove spec.k \
  --definition auditor-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.get-odd-collatz
entry_exit=$?
printf 'get_odd_collatz_kprove_exit=%s\n' "$entry_exit"

kprove spec.k \
  --definition auditor-verification-kompiled \
  --spec-module SPEC
all_exit=$?
printf 'all_spec_claims_kprove_exit=%s\n' "$all_exit"

if [[ "$loop_exit" -ne 0 || "$entry_exit" -ne 0 || "$all_exit" -ne 0 ]]; then
  exit 1
fi
