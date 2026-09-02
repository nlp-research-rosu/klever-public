#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/11-string-xor/body-mutation
definition="$work/body-verification-kompiled"

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  return "$status"
}

run python3 /audit-output/evidence/make_body_mutation.py
status=$?
[ "$status" -eq 0 ] || exit "$status"

run sha256sum \
  /tmp/audit-work/11-string-xor/candidate/verification.k \
  "$work/verification.k" \
  /audit-output/evidence/body-mutation-verification.k
status=$?
[ "$status" -eq 0 ] || exit "$status"

cd "$work" || exit 1
run kompile verification.k \
  --backend haskell \
  --main-module STRING-XOR-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$definition"
build_status=$?
[ "$build_status" -eq 0 ] || exit "$build_status"

printf 'COMMAND: timeout 180 kprove audit-original-pinning-spec.k --definition %q --spec-module AUDIT-BODY-PINNING\n' \
  "$definition"
timeout 180 kprove audit-original-pinning-spec.k \
  --definition "$definition" \
  --spec-module AUDIT-BODY-PINNING \
  > "$work/body-pinning.raw.log" 2>&1
pinning_status=$?
sed -n '1,220p' "$work/body-pinning.raw.log"
printf 'EXIT_STATUS: %s\n' "$pinning_status"
grep -q 'WarnStuckClaimState' "$work/body-pinning.raw.log"
pinning_stuck=$?
printf 'EXPECTED_STUCK_PRESENT: %s\n' "$pinning_stuck"

printf 'COMMAND: timeout 180 kprove spec.k --definition %q --spec-module STRING-XOR-SPEC --claims STRING-XOR-SPEC.loop-invariant,STRING-XOR-SPEC.solution-correct\n' \
  "$definition"
timeout 180 kprove spec.k \
  --definition "$definition" \
  --spec-module STRING-XOR-SPEC \
  --claims STRING-XOR-SPEC.loop-invariant,STRING-XOR-SPEC.solution-correct \
  > "$work/body-proof.raw.log" 2>&1
proof_status=$?
sed -n '1,260p' "$work/body-proof.raw.log"
printf 'EXIT_STATUS: %s\n' "$proof_status"
grep -q 'WarnStuckClaimState' "$work/body-proof.raw.log"
proof_stuck=$?
printf 'EXPECTED_STUCK_PRESENT: %s\n' "$proof_stuck"

if [ "$pinning_status" -eq 0 ] || [ "$pinning_stuck" -ne 0 ]; then
  exit 1
fi
if [ "$proof_status" -eq 0 ] || [ "$proof_stuck" -ne 0 ]; then
  exit 1
fi
printf 'BODY_SENSITIVITY_OK\n'
exit 0
