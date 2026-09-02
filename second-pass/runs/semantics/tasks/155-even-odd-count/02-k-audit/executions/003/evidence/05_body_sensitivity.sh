#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run_expected_failure() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d; expected nonzero]\n' "$status"
  test "$status" -ne 0
}

mutant=/tmp/audit-work/body-mutation
run mkdir -p "$mutant/reference-semantics" || exit $?
run cp -a /reference/reference-semantics/. "$mutant/reference-semantics/" || exit $?
run cp /candidate/spec.k "$mutant/spec.k" || exit $?

printf '$ sed s/CmpOp\\(\"==\",\\ Int\\(0\\)\\)/CmpOp\\(\"==\",\\ Int\\(1\\)\\)/ /candidate/verification.k > /tmp/audit-work/body-mutation/verification.k\n'
sed 's/CmpOp("==", Int(0))/CmpOp("==", Int(1))/' /candidate/verification.k > "$mutant/verification.k"
status=$?
printf '[exit %d]\n' "$status"
test "$status" -eq 0 || exit "$status"
run cp "$mutant/verification.k" /audit-output/evidence/05_verification_body_mutant.k || exit $?
run diff -u /candidate/verification.k "$mutant/verification.k" || true

kpath="/home/agent/.nix-profile/bin:$PATH"
run env PATH="$kpath" kompile "$mutant/verification.k" \
  --backend haskell \
  --main-module EVEN-ODD-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$mutant/verification-base-kompiled" || exit $?

run_expected_failure env PATH="$kpath" kprove "$mutant/spec.k" \
  --definition "$mutant/verification-base-kompiled" \
  --spec-module EVEN-ODD-LOOP-SPEC || exit $?

run env PATH="$kpath" kompile "$mutant/verification.k" \
  --backend haskell \
  --main-module EVEN-ODD-VERIFICATION-SUMMARY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$mutant/verification-kompiled" || exit $?

run env PATH="$kpath" kprove "$mutant/spec.k" \
  --definition "$mutant/verification-kompiled" \
  --spec-module EVEN-ODD-SPEC || exit $?
