#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/source || exit 99

echo "Independently selected helper claim:"
run kprove spec.k \
  --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module SPEC \
  --claims SPEC.encrypt-call-correct
helper_status=$?

echo "Complete target spec (helper plus dependent program-correct claim):"
run kprove spec.k \
  --definition /tmp/audit-work/build/proof-kompiled \
  --spec-module SPEC
all_status=$?

printf 'summary helper=%d all=%d\n' "$helper_status" "$all_status"
if (( helper_status != 0 || all_status != 0 )); then
  exit 1
fi
