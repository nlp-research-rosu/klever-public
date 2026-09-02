#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/final-validation.log

{
  printf '%s\n' '$ tail -n 2 /audit-output/REVIEW.md'
  tail -n 2 /audit-output/REVIEW.md
  printf '\n%s\n' '$ rg -c "^VERDICT:|^LEGITIMACY:" /audit-output/REVIEW.md'
  rg -c '^VERDICT:|^LEGITIMACY:' /audit-output/REVIEW.md
  printf '\n%s\n' '$ rg -n "^VERDICT: PASS$|^LEGITIMACY: LEGIT$" /audit-output/REVIEW.md'
  rg -n '^VERDICT: PASS$|^LEGITIMACY: LEGIT$' /audit-output/REVIEW.md
  printf '\n%s\n' '$ rg -n "all_checks_pass.*true|failed_checks" structural-audit.log'
  rg -n '"all_checks_pass": true|"failed_checks"' \
    /audit-output/evidence/structural-audit.log
  printf '\n%s\n' '$ tail -n 1 successful command logs'
  tail -n 1 /audit-output/evidence/structural-audit.log
  tail -n 1 \
    /audit-output/evidence/preflight-check-generation-repaired.log
  printf '\n%s\n' '$ test ! -e /candidate'
  test ! -e /candidate
  code=$?
  printf 'TEST_EXIT_CODE: %s\n' "$code"
  exit "$code"
} >"$log" 2>&1
