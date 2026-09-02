#!/usr/bin/env bash
set -u

work=/tmp/audit-work/final-reconstruction
cp /audit-output/evidence/spec-false-result.k \
  /audit-output/evidence/verification-body-mutation.k \
  /audit-output/evidence/spec-body-mutation.k \
  "$work/"
cd "$work" || exit 1

echo '$ kprove spec-false-result.k --definition verification-audit-kompiled --spec-module ROMAN-SPEC-FALSE-RESULT'
kprove spec-false-result.k \
  --definition verification-audit-kompiled \
  --spec-module ROMAN-SPEC-FALSE-RESULT
false_status=$?
echo "EXIT_STATUS=$false_status"
if test "$false_status" -eq 0; then
  echo 'UNEXPECTED: false result mutation proved'
  exit 1
fi
echo 'EXPECTED_FAILURE=false result obligation rejected'

echo '$ kompile verification-body-mutation.k --backend haskell --main-module BODY-SENSITIVITY --syntax-module MINI-PYTHON-SYNTAX --output-definition body-mutation-audit-kompiled'
kompile verification-body-mutation.k \
  --backend haskell \
  --main-module BODY-SENSITIVITY \
  --syntax-module MINI-PYTHON-SYNTAX \
  --output-definition body-mutation-audit-kompiled
build_status=$?
echo "EXIT_STATUS=$build_status"
test "$build_status" -eq 0 || exit "$build_status"

echo '$ kprove spec-body-mutation.k --definition body-mutation-audit-kompiled --spec-module BODY-SENSITIVITY-SPEC'
kprove spec-body-mutation.k \
  --definition body-mutation-audit-kompiled \
  --spec-module BODY-SENSITIVITY-SPEC
body_status=$?
echo "EXIT_STATUS=$body_status"
if test "$body_status" -eq 0; then
  echo 'UNEXPECTED: changed executable body proved the old result'
  exit 1
fi
echo 'EXPECTED_FAILURE=mutated body returned "wrong" instead of "ix"'
exit 0
