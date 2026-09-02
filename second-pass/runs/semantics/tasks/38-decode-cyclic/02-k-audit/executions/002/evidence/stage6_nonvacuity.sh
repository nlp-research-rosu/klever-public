#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/38-decode-cyclic
log=/audit-output/evidence/stage6_nonvacuity.log

{
  cd "$scratch" || exit 1

  echo '$ python3 /audit-output/evidence/make_vacuity_mutant.py'
  python3 /audit-output/evidence/make_vacuity_mutant.py
  make_status=$?
  echo "EXIT_STATUS=$make_status"
  (( make_status == 0 )) || exit 1

  echo
  echo '$ kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run'
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY \
    --dry-run
  dry_status=$?
  echo "EXIT_STATUS=$dry_status"
  (( dry_status == 0 )) || exit 1

  echo
  echo '$ kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY'
  kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY
  prove_status=$?
  echo "EXIT_STATUS=$prove_status"
  if (( prove_status == 0 )); then
    echo 'ERROR: false result mutation unexpectedly proved'
    exit 1
  fi
  echo 'EXPECTED_UNMET_RESULT_OBLIGATION=1'
  exit 0
} >"$log" 2>&1
