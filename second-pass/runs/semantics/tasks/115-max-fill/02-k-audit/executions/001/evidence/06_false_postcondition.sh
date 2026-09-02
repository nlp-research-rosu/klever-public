#!/usr/bin/env bash
set -u
set -o pipefail

WORK=/tmp/audit-work/115-max-fill
SPEC=/audit-output/evidence/06_false_postcondition.k

cd "$WORK" || exit 125

printf 'COMMAND: timeout 300s kprove %q -I %q --definition verification-kompiled --spec-module MAX-FILL-SPEC-VACUITY --dry-run\n' "$SPEC" "$WORK"
timeout 300s kprove "$SPEC" \
  -I "$WORK" \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC-VACUITY \
  --dry-run
build_status=$?
printf 'EXIT_STATUS: %s\n\n' "$build_status"
if [[ "$build_status" -ne 0 ]]; then
  exit "$build_status"
fi

printf 'COMMAND: timeout 600s kprove %q -I %q --definition verification-kompiled --spec-module MAX-FILL-SPEC-VACUITY\n' "$SPEC" "$WORK"
timeout 600s kprove "$SPEC" \
  -I "$WORK" \
  --definition verification-kompiled \
  --spec-module MAX-FILL-SPEC-VACUITY
proof_status=$?
printf 'EXIT_STATUS: %s\n' "$proof_status"
if [[ "$proof_status" -eq 0 || "$proof_status" -eq 124 ]]; then
  exit 1
fi
exit 0
