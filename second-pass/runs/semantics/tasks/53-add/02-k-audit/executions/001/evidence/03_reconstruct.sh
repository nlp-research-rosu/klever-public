#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/03_reconstruct.log
WORK=/tmp/audit-work/53-add
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

run command -v kompile || exit $?
run command -v krun || exit $?
run command -v kprove || exit $?
run kompile --version || exit $?
run krun --version || exit $?
run kprove --version || exit $?

printf '\n$ cd %q\n' "$WORK"
cd "$WORK" || exit 1
printf '[exit 0]\n'

run rm -rf \
  /tmp/audit-work/53-add/runtime-kompiled \
  /tmp/audit-work/53-add/verification-kompiled

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled || exit $?

run krun concrete-tests.mpy --definition runtime-kompiled || exit $?

run kompile verification.k \
  --backend haskell \
  --main-module ADD-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled || exit $?

run kprove spec.k \
  --definition verification-kompiled \
  --spec-module ADD-SPEC
proof_rc=$?

printf '\nProof success predicates:\n'
if grep -Fxq '#Top' "$LOG"; then
  printf '#Top exact line present: yes\n'
else
  printf '#Top exact line present: no\n'
fi
printf 'kprove exit: %d\n' "$proof_rc"
exit "$proof_rc"
