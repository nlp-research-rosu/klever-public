#!/usr/bin/env bash
set -u
set -o pipefail
PS4='+ command: '
set -x

cd /tmp/audit-work/candidate

# This target proves the auxiliary circularity itself.
kprove spec.k \
  --definition auditor-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.collatz-loop
loop_exit=$?
printf 'collatz_loop_kprove_exit=%s\n' "$loop_exit"

# This target proves both claims together, making the established loop
# circularity available while checking the entry theorem.
kprove spec.k \
  --definition auditor-verification-kompiled \
  --spec-module SPEC
all_exit=$?
printf 'complete_spec_kprove_exit=%s\n' "$all_exit"

if [[ "$loop_exit" -ne 0 || "$all_exit" -ne 0 ]]; then
  exit 1
fi
