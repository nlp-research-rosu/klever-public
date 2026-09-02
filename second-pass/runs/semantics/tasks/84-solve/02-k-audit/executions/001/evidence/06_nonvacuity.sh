#!/usr/bin/env bash
set -u
set -o pipefail

definition=/tmp/audit-work/candidate-src/verification-kompiled
mutation=/audit-output/evidence/06_spec_vacuity.k
dry_log=/tmp/audit-work/vacuity-dry-run.log
proof_log=/tmp/audit-work/vacuity-proof.log

printf 'Satisfying false-mutation witness: N=0\n'
printf 'Python program result: "0"; mutated required result: binaryNumeral(1) = "1"\n'

printf '\n$ kprove %s --definition %s --spec-module SPEC-VACUITY --dry-run\n' \
  "$mutation" "$definition"
kprove "$mutation" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY \
  --dry-run \
  > "$dry_log" 2>&1
dry_rc=$?
printf '[exit %d]\n' "$dry_rc"
printf 'dry-run-log-bytes='
wc -c < "$dry_log"
tail -n 20 "$dry_log"

printf '\n$ kprove %s --definition %s --spec-module SPEC-VACUITY --output pretty\n' \
  "$mutation" "$definition"
kprove "$mutation" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY \
  --output pretty \
  |& tee "$proof_log"
proof_rc=${PIPESTATUS[0]}
printf '[exit %d]\n' "$proof_rc"

printf '$ cp -a %s /audit-output/evidence/06_vacuity_proof_raw.log\n' "$proof_log"
cp -a "$proof_log" /audit-output/evidence/06_vacuity_proof_raw.log
copy_rc=$?
printf '[exit %d]\n' "$copy_rc"

printf '$ grep -q WarnStuckClaimState %s\n' "$proof_log"
grep -q WarnStuckClaimState "$proof_log"
stuck_rc=$?
printf '[exit %d]\n' "$stuck_rc"

if (( dry_rc == 0 && proof_rc != 0 && copy_rc == 0 && stuck_rc == 0 )); then
  printf 'NONVACUITY_CHECK=PASS\n'
  exit 0
fi
printf 'NONVACUITY_CHECK=FAIL\n'
exit 1
