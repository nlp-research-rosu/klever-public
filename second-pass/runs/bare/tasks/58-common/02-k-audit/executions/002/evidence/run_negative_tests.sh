#!/usr/bin/env bash
set -u -o pipefail

root=/tmp/audit-work/58-common-audit
definition="$root/verification-kompiled-audit"
overall=0

run_expected_failure() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if [[ "$status" -eq 0 ]]; then
    printf 'UNEXPECTED_SUCCESS\n'
    overall=1
  else
    printf 'EXPECTED_NONZERO\n'
  fi
}

run_expected_failure \
  kprove "$root/audit-body-mutation.k" \
  --definition "$definition" \
  --spec-module AUDIT-BODY-MUTATION

run_expected_failure \
  kprove "$root/audit-false-post.k" \
  --definition "$definition" \
  --spec-module AUDIT-FALSE-POST

printf '\nOVERALL_EXIT=%d\n' "$overall"
exit "$overall"
