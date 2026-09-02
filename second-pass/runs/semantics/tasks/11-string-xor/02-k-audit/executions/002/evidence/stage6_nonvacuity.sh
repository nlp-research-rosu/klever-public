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

run python3 /audit-output/evidence/nonvacuity_witness.py
witness_status=$?
[ "$witness_status" -eq 0 ] || exit "$witness_status"

cd "$work" || exit 1
run kprove /audit-output/evidence/spec-vacuity.k \
  --definition "$definition" \
  -I "$work" \
  --spec-module STRING-XOR-SPEC-VACUITY \
  --claims STRING-XOR-SPEC-VACUITY.loop-invariant,STRING-XOR-SPEC-VACUITY.false-solution \
  --dry-run
build_status=$?
[ "$build_status" -eq 0 ] || exit "$build_status"

printf 'COMMAND: timeout 180 kprove /audit-output/evidence/spec-vacuity.k --definition %q -I %q --spec-module STRING-XOR-SPEC-VACUITY --claims STRING-XOR-SPEC-VACUITY.loop-invariant,STRING-XOR-SPEC-VACUITY.false-solution\n' \
  "$definition" "$work"
timeout 180 kprove /audit-output/evidence/spec-vacuity.k \
  --definition "$definition" \
  -I "$work" \
  --spec-module STRING-XOR-SPEC-VACUITY \
  --claims STRING-XOR-SPEC-VACUITY.loop-invariant,STRING-XOR-SPEC-VACUITY.false-solution \
  > /tmp/audit-work/11-string-xor/nonvacuity.raw.log 2>&1
proof_status=$?
sed -n '1,300p' /tmp/audit-work/11-string-xor/nonvacuity.raw.log
printf 'EXIT_STATUS: %s\n' "$proof_status"
grep -q 'WarnStuckClaimState' /tmp/audit-work/11-string-xor/nonvacuity.raw.log
stuck_status=$?
printf 'EXPECTED_STUCK_PRESENT: %s\n' "$stuck_status"

if [ "$proof_status" -eq 0 ] || [ "$stuck_status" -ne 0 ]; then
  exit 1
fi
printf 'NONVACUITY_OK\n'
exit 0
