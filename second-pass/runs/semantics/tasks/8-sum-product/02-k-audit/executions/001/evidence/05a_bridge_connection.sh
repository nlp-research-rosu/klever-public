#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/reconstruction
cd "$WORK" || exit 99

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  return 0
}

run cp /audit-output/evidence/bridge-universal-spec.k \
  "$WORK/bridge-universal-spec.k"

printf '\nBRIDGE_FREE_UNIVERSAL_CONNECTION_THEOREM\n'
run kprove bridge-universal-spec.k \
  --definition verification-kompiled \
  --spec-module LOOP-BRIDGE-UNIVERSAL-CONNECTION \
  --output pretty
