#!/usr/bin/env bash
set -u
export PATH="/home/agent/.nix-profile/bin:$PATH"
work=/tmp/audit-work/candidate
definition="$work/verification-body-mut-kompiled"

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return "$rc"
}

run test ! -e "$definition" || exit $?
run kompile "$work/verification-body-mut.k" \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUT \
  --syntax-module MPY-SYNTAX \
  --output-definition "$definition" || exit $?
printf '%s\n' 'SATISFYING WITNESS: LIST1 = pyStr("") :: .StrVals; LIST2 = pyStr("a") :: .StrVals; totals 0 < 1.'
run kprove "$work/spec-body-mut.k" \
  --definition "$definition" \
  --spec-module SPEC-BODY-MUT \
  --claims SPEC-BODY-MUT.mutated-first-lt
proof_rc=$?
if [[ "$proof_rc" -eq 0 ]]; then
  printf '%s\n' 'UNEXPECTED: body-mutated false claim closed'
  exit 1
fi
printf '%s\n' 'EXPECTED_BODY_SENSITIVITY_FAILURE'
