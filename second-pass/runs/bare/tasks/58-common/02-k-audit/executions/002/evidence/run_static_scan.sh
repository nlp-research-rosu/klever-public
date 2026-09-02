#!/usr/bin/env bash
set -u -o pipefail

candidate=/tmp/audit-work/58-common-audit/candidate

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

overall=0
run rg -n \
  '^[[:space:]]*(requires|module|imports|configuration|syntax|rule|claim)|\[(function|total|functional|simplification|concrete|priority|owise|anywhere|macro)' \
  "$candidate/semantic.k" "$candidate/verification.k" "$candidate/spec.k" || overall=1
run nl -ba "$candidate/semantic.k" || overall=1
run nl -ba "$candidate/verification.k" || overall=1
run nl -ba "$candidate/spec.k" || overall=1
printf '\nOVERALL_EXIT=%d\n' "$overall"
exit "$overall"
