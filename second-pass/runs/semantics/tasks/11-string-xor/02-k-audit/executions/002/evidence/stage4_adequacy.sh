#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/11-string-xor/candidate
definition="$work/audit-verification-kompiled"

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  return "$status"
}

run python3 /audit-output/evidence/generate_pinning_spec.py
status=$?
[ "$status" -eq 0 ] || exit "$status"

run sha256sum \
  /tmp/audit-work/11-string-xor/regenerated-solution.mpy \
  "$work/solution.mpy" \
  "$work/audit-pinning-spec.k"
status=$?
[ "$status" -eq 0 ] || exit "$status"

cd "$work" || exit 1
run timeout 180 kprove audit-pinning-spec.k \
  --definition "$definition" \
  --spec-module AUDIT-PINNING-SPEC
pinning_status=$?

run timeout 180 kprove /audit-output/evidence/adequacy-ground.k \
  --definition "$definition" \
  -I "$work" \
  --spec-module AUDIT-ADEQUACY-GROUND
ground_status=$?

printf 'ADEQUACY_STATUS constructor-pinning=%s ground-witnesses=%s\n' \
  "$pinning_status" "$ground_status"
[ "$pinning_status" -eq 0 ] && [ "$ground_status" -eq 0 ]
exit $?
