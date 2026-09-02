#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/06_nonvacuity.log
WORK=/tmp/audit-work/53-add
MUTATION="$WORK/spec-vacuity-audit.k"
DRY_OUT="$WORK/spec-vacuity-audit.dry-run.out"
PROOF_OUT="$WORK/spec-vacuity-audit.kprove.out"
export PATH="/home/agent/.nix-profile/bin:$PATH"
exec >"$LOG" 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

run cp /audit-output/evidence/spec-vacuity-audit.k "$MUTATION" || exit $?

printf '\n$ cd %q\n' "$WORK"
cd "$WORK" || exit 1
printf '[exit 0]\n'

printf '\n$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module ADD-SPEC-VACUITY-AUDIT --dry-run > %s 2>&1\n' "$DRY_OUT"
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module ADD-SPEC-VACUITY-AUDIT \
  --dry-run >"$DRY_OUT" 2>&1
dry_rc=$?
printf '[exit %d]\n' "$dry_rc"
run wc -c "$DRY_OUT"
run sed -n 1,80p "$DRY_OUT"

printf '\n$ kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module ADD-SPEC-VACUITY-AUDIT > %s 2>&1\n' "$PROOF_OUT"
kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module ADD-SPEC-VACUITY-AUDIT >"$PROOF_OUT" 2>&1
proof_rc=$?
printf '[exit %d]\n' "$proof_rc"
run wc -c "$PROOF_OUT"
run sed -n 1,240p "$PROOF_OUT"

printf '\nExpected-result checks:\n'
printf 'dry-run build exit == 0: %s\n' "$([ "$dry_rc" -eq 0 ] && printf yes || printf no)"
printf 'false proof exit != 0: %s\n' "$([ "$proof_rc" -ne 0 ] && printf yes || printf no)"
if grep -q 'WarnStuckClaimState' "$PROOF_OUT"; then
  printf 'WarnStuckClaimState present: yes\n'
else
  printf 'WarnStuckClaimState present: no\n'
fi
if grep -q '5 ~> .K' "$PROOF_OUT" && grep -q '#callAdd(2, 3) => 6' "$MUTATION"; then
  printf 'actual 5 versus required 6 visible: yes\n'
else
  printf 'actual 5 versus required 6 visible: no\n'
fi

if [ "$dry_rc" -eq 0 ] && [ "$proof_rc" -ne 0 ] && grep -q 'WarnStuckClaimState' "$PROOF_OUT"; then
  exit 0
fi
exit 1
