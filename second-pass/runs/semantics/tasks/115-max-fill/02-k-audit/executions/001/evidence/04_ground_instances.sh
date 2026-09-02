#!/usr/bin/env bash
set -u
set -o pipefail

WORK=/tmp/audit-work/115-max-fill
SPEC=/audit-output/evidence/04_ground_instances.k
overall=0

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n\n' "$status"
  if [[ "$status" -ne 0 ]]; then
    overall=1
  fi
  return 0
}

cd "$WORK" || exit 125
run timeout 300s kprove "$SPEC" \
  -I "$WORK" \
  --definition verification-kompiled \
  --spec-module MAX-FILL-GROUND-INSTANCES
for label in ground-empty ground-single-one ground-two-rows; do
  run timeout 300s kprove "$SPEC" \
    -I "$WORK" \
    --definition verification-kompiled \
    --spec-module MAX-FILL-GROUND-INSTANCES \
    --claims "MAX-FILL-GROUND-INSTANCES.$label"
done
exit "$overall"
