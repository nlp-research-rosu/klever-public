#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/38-decode-cyclic
log=/audit-output/evidence/stage4_body_sensitivity.log

{
  cd "$scratch" || exit 1

  echo '$ python3 /audit-output/evidence/make_body_mutant.py'
  python3 /audit-output/evidence/make_body_mutant.py
  make_status=$?
  echo "EXIT_STATUS=$make_status"
  (( make_status == 0 )) || exit 1

  echo
  echo '$ kompile verification-body-mutant.k --backend haskell --main-module VERIFICATION-BODY-MUTANT --syntax-module MPY-SYNTAX --output-definition verification-body-mutant-kompiled'
  kompile verification-body-mutant.k \
    --backend haskell \
    --main-module VERIFICATION-BODY-MUTANT \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-body-mutant-kompiled
  build_status=$?
  echo "EXIT_STATUS=$build_status"
  (( build_status == 0 )) || exit 1

  echo
  echo '$ kprove spec-body-mutant.k --definition verification-body-mutant-kompiled --spec-module SPEC-BODY-MUTANT'
  kprove spec-body-mutant.k \
    --definition verification-body-mutant-kompiled \
    --spec-module SPEC-BODY-MUTANT
  prove_status=$?
  echo "EXIT_STATUS=$prove_status"
  if (( prove_status == 0 )); then
    echo 'ERROR: body mutant unexpectedly proved'
    exit 1
  fi
  echo 'EXPECTED_FAILURE_CONFIRMED=1'
  exit 0
} >"$log" 2>&1
