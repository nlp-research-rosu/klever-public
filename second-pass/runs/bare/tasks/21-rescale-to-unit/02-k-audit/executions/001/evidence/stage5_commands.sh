#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run rg -n '^\s*(syntax|configuration|rule|claim)' \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/verification.k \
  /tmp/audit-work/source/spec.k
run rg -n '\[(function|functional|total|simplification|priority|owise|concrete|trusted|macro|anywhere)' \
  /tmp/audit-work/source/semantic.k \
  /tmp/audit-work/source/verification.k \
  /tmp/audit-work/source/spec.k

run krun /tmp/audit-work/source/solution.mpy \
  --definition /tmp/audit-work/build/semantic-kompiled \
  -cARGS='vlist(-9007199254740992, 1, 9007199254740992)' \
  --output pretty
run python3 /audit-output/evidence/semantic_gap.py
