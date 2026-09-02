#!/usr/bin/env bash
set -uo pipefail
PS4='+ ${BASH_SOURCE##*/}:${LINENO}: '
set -x

cd /tmp/audit-work/34-unique

kprove spec-symbolic.k \
  --definition proof-kompiled \
  --spec-module SPEC-SYMBOLIC
symbolic_status=$?

kprove spec-example.k \
  --definition proof-kompiled \
  --spec-module SPEC-EXAMPLE
example_status=$?

set +x
printf 'SYMBOLIC_CLAIM_EXIT_STATUS=%s\n' "$symbolic_status"
printf 'EXAMPLE_CLAIM_EXIT_STATUS=%s\n' "$example_status"
if (( symbolic_status || example_status )); then
  exit 1
fi
exit 0
