#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence

cp "$evidence/verification-body-mutated.k" "$work/"
cp "$evidence/spec-body-sensitivity.k" "$work/"

printf '%s\n' \
  'COMMAND: diff -u verification.k verification-body-mutated.k' \
  'CWD: /tmp/audit-work/reconstruction' \
  'EXPECTED: nonzero because this displays the deliberate source mutation'
(
  cd "$work" || exit 99
  diff -u verification.k verification-body-mutated.k
)
diff_status=$?
printf 'EXIT_STATUS: %s\n' "$diff_status"

printf '%s\n' \
  'COMMAND: kompile verification-body-mutated.k --backend haskell --main-module VERIFICATION-BODY-MUTATED --syntax-module VERIFICATION-BODY-MUTATED --output-definition verification-body-mutated-kompiled' \
  'CWD: /tmp/audit-work/reconstruction'
(
  cd "$work" || exit 99
  kompile verification-body-mutated.k \
    --backend haskell \
    --main-module VERIFICATION-BODY-MUTATED \
    --syntax-module VERIFICATION-BODY-MUTATED \
    --output-definition verification-body-mutated-kompiled
)
build_status=$?
printf 'EXIT_STATUS: %s\n' "$build_status"

printf '%s\n' \
  'COMMAND: kprove spec-body-sensitivity.k --definition verification-body-mutated-kompiled --spec-module SPEC-BODY-SENSITIVITY' \
  'CWD: /tmp/audit-work/reconstruction' \
  'EXPECTED: nonzero stuck claim; witness N=8 makes mutated body false but original postcondition true'
(
  cd "$work" || exit 99
  kprove spec-body-sensitivity.k \
    --definition verification-body-mutated-kompiled \
    --spec-module SPEC-BODY-SENSITIVITY
)
proof_status=$?
printf 'EXIT_STATUS: %s\n' "$proof_status"

if (( build_status != 0 )); then
  exit 1
fi
if (( proof_status == 0 )); then
  exit 1
fi
exit 0
