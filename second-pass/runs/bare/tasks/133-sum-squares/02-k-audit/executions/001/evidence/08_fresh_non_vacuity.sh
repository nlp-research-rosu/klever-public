#!/usr/bin/env bash
set -u

log=/audit-output/evidence/08_fresh_non_vacuity.log
exec > >(tee "$log") 2>&1
scratch=/tmp/audit-work/133-sum-squares
capture="$scratch/.audit-command-output.log"

show_bounded() {
  lines=$(wc -l <"$capture")
  bytes=$(wc -c <"$capture")
  printf 'OUTPUT_LINES: %d OUTPUT_BYTES: %d\n' "$lines" "$bytes"
  if (( lines <= 260 )); then
    sed -n '1,260p' "$capture"
  else
    sed -n '1,200p' "$capture"
    printf '[... bounded log omitted %d middle lines ...]\n' "$((lines - 260))"
    tail -60 "$capture"
  fi
}

printf 'SATISFYING_FALSE_WITNESS: L=nil; actual=0; mutated_postcondition=1\n'
printf '\nCOMMAND: cp /audit-output/evidence/spec-vacuity-audit.k %q/spec-vacuity-audit.k\n' "$scratch"
cp /audit-output/evidence/spec-vacuity-audit.k "$scratch/spec-vacuity-audit.k"
copy_status=$?
printf 'EXIT_STATUS: %d\n' "$copy_status"

printf 'COMMAND: cd %q\n' "$scratch"
cd "$scratch"
printf 'EXIT_STATUS: %d\n' "$?"

printf '\nCOMMAND: kprove spec-vacuity-audit.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run\n'
kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run >"$capture" 2>&1
dry_status=$?
show_bounded
printf 'EXIT_STATUS: %d\n' "$dry_status"

printf '\nCOMMAND: kprove spec-vacuity-audit.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY-AUDIT\n'
kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT >"$capture" 2>&1
proof_status=$?
show_bounded
printf 'EXIT_STATUS: %d\n' "$proof_status"

grep -q 'WarnStuckClaimState' "$capture"
stuck_status=$?
grep -Eq 'implication check.*failed|cannot be rewritten further' "$capture"
obligation_status=$?
printf 'CHECK: WarnStuckClaimState EXIT_STATUS: %d\n' "$stuck_status"
printf 'CHECK: unmet-obligation diagnostic EXIT_STATUS: %d\n' "$obligation_status"

if (( copy_status == 0 && dry_status == 0 && proof_status != 0
      && stuck_status == 0 && obligation_status == 0 )); then
  printf 'EXPECTED_FAILURE_CONFIRMED: yes\n'
  exit 0
fi
printf 'EXPECTED_FAILURE_CONFIRMED: no\n'
exit 1
