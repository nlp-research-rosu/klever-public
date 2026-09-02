#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/05_body_sensitivity.log
WORK=/tmp/audit-work/53-add
DEF="$WORK/body-mutation-kompiled"
PROOF_OUT="$WORK/spec-body-mutation.kprove.out"
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

run cp /audit-output/evidence/verification-body-mutation.k "$WORK/verification-body-mutation.k" || exit $?
run cp /audit-output/evidence/spec-body-mutation.k "$WORK/spec-body-mutation.k" || exit $?
run rm -rf /tmp/audit-work/53-add/body-mutation-kompiled

printf '\n$ cd %q\n' "$WORK"
cd "$WORK" || exit 1
printf '[exit 0]\n'

run kompile verification-body-mutation.k \
  --backend haskell \
  --main-module ADD-VERIFICATION-BODY-MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutation-kompiled || exit $?

printf '\n$ kprove spec-body-mutation.k --definition body-mutation-kompiled --spec-module ADD-SPEC-BODY-MUTATION > %s 2>&1\n' "$PROOF_OUT"
kprove spec-body-mutation.k \
  --definition body-mutation-kompiled \
  --spec-module ADD-SPEC-BODY-MUTATION >"$PROOF_OUT" 2>&1
proof_rc=$?
printf '[exit %d]\n' "$proof_rc"
run wc -c "$PROOF_OUT"
run sed -n 1,220p "$PROOF_OUT"

printf '\nExpected body-sensitivity checks:\n'
printf 'mutated proof exit != 0: %s\n' "$([ "$proof_rc" -ne 0 ] && printf yes || printf no)"
if grep -q -- '-1 ~> .K' "$PROOF_OUT" && grep -q '#callAddBodyMutation(2, 3) => 5' "$WORK/spec-body-mutation.k"; then
  printf 'mutated body result -1 versus required 5 visible: yes\n'
else
  printf 'mutated body result -1 versus required 5 visible: no\n'
fi
if grep -q 'WarnStuckClaimState' "$PROOF_OUT"; then
  printf 'WarnStuckClaimState present: yes\n'
else
  printf 'WarnStuckClaimState present: no\n'
fi

if [ "$proof_rc" -ne 0 ] && grep -q 'WarnStuckClaimState' "$PROOF_OUT" && grep -q -- '-1 ~> .K' "$PROOF_OUT"; then
  exit 0
fi
exit 1
