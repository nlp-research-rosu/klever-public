#!/usr/bin/env bash
set -u

report=/audit-output/REVIEW.md
status=0

expected_tail=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
actual_tail=$(tail -n 2 "$report")
if [[ "$actual_tail" == "$expected_tail" ]]; then
  printf 'FINAL_MARKERS: exact\n'
else
  printf 'FINAL_MARKERS: mismatch\n'
  status=1
fi

verdict_count=$(grep -c '^VERDICT:' "$report")
legitimacy_count=$(grep -c '^LEGITIMACY:' "$report")
printf 'VERDICT_MARKER_COUNT: %s\n' "$verdict_count"
printf 'LEGITIMACY_MARKER_COUNT: %s\n' "$legitimacy_count"
if [[ "$verdict_count" -ne 1 || "$legitimacy_count" -ne 1 ]]; then
  status=1
fi

for stage in 1 2 3 4 5 6 7; do
  if grep -q "^## $stage\\." "$report"; then
    printf 'STAGE_%d: present\n' "$stage"
  else
    printf 'STAGE_%d: missing\n' "$stage"
    status=1
  fi
done

mapfile -t evidence_refs < <(
  grep -o 'evidence/[A-Za-z0-9_.-]*' "$report" | LC_ALL=C sort -u
)
for relative in "${evidence_refs[@]}"; do
  if [[ -f "/audit-output/$relative" ]]; then
    printf 'EVIDENCE_PRESENT: %s\n' "$relative"
  else
    printf 'EVIDENCE_MISSING: %s\n' "$relative"
    status=1
  fi
done

printf 'VALIDATION_STATUS: %d\n' "$status"
exit "$status"
