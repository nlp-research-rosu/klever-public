#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md
evidence=/audit-output/evidence
failures=0

expected_tail=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
actual_tail=$(tail -n 2 "$review")
if [ "$actual_tail" = "$expected_tail" ]; then
  printf 'FINAL_MARKERS_OK\n'
else
  printf 'FINAL_MARKERS_BAD\n'
  failures=$((failures + 1))
fi

verdict_count=$(grep -c '^VERDICT:' "$review")
legitimacy_count=$(grep -c '^LEGITIMACY:' "$review")
printf 'VERDICT_MARKER_COUNT: %d\n' "$verdict_count"
printf 'LEGITIMACY_MARKER_COUNT: %d\n' "$legitimacy_count"
if [ "$verdict_count" -ne 1 ] || [ "$legitimacy_count" -ne 1 ]; then
  failures=$((failures + 1))
fi

printf 'EVIDENCE_REFERENCE_CHECK_BEGIN\n'
while IFS= read -r relative; do
  if [ -e "/audit-output/$relative" ]; then
    printf 'PRESENT: %s\n' "$relative"
  else
    printf 'MISSING: %s\n' "$relative"
    failures=$((failures + 1))
  fi
done < <(grep -oE 'evidence/[A-Za-z0-9._-]+' "$review" | sort -u)
printf 'EVIDENCE_REFERENCE_CHECK_END\n'

symlink_count=$(find -P "$evidence" -maxdepth 1 -type l -print | wc -l)
printf 'EVIDENCE_SYMLINK_COUNT: %d\n' "$symlink_count"
if [ "$symlink_count" -ne 0 ]; then
  failures=$((failures + 1))
fi

for log in "$evidence"/*.log; do
  case "$log" in
    "$evidence/21-final-validation.log") continue ;;
  esac
  first=$(sed -n '1p' "$log")
  last=$(tail -n 1 "$log")
  if [[ "$first" != COMMAND:* ]] || [[ "$last" != EXIT_STATUS:* ]]; then
    printf 'MALFORMED_LOG: %s\n' "$(basename "$log")"
    failures=$((failures + 1))
  fi
done

printf 'VALIDATION_FAILURE_COUNT: %d\n' "$failures"
exit "$failures"
