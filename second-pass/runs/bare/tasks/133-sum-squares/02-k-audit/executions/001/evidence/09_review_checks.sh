#!/usr/bin/env bash
set -u

log=/audit-output/evidence/09_review_checks.log
exec > >(tee "$log") 2>&1

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

run tail -n 2 /audit-output/REVIEW.md
run test "$(tail -n 2 /audit-output/REVIEW.md)" = \
  $'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
run test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" = 1
run test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" = 1
run wc -lc /audit-output/REVIEW.md
run find /audit-output/evidence -maxdepth 1 -type f -printf '%f %s bytes\n'
