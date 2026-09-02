#!/usr/bin/env bash
set -u

output=/audit-output/evidence/06-vacuity-dry-run.kore
printf '%s\n' \
  'INNER_COMMAND: /usr/bin/kprove spec-vacuity.k --definition /tmp/audit-work/69-search-audit/build/verification-kompiled --spec-module SPEC-VACUITY --dry-run'
/usr/bin/kprove spec-vacuity.k \
  --definition /tmp/audit-work/69-search-audit/build/verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run > "$output"
status=$?
printf 'dry-run output: %s\n' "$output"
wc -lc "$output"
printf 'dry-run exit status: %d\n' "$status"
exit "$status"
