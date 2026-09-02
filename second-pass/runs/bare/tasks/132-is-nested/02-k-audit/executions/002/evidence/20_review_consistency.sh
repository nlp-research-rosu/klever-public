#!/usr/bin/env bash
set -euo pipefail

expected=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
actual=$(tail -n 2 /audit-output/REVIEW.md)
[[ "$actual" == "$expected" ]]

for stage in 1 2 3 4 5 6 7; do
  rg -q "^## ${stage}\\." /audit-output/REVIEW.md
done

missing=0
while IFS= read -r relative; do
  if [[ ! -f "/audit-output/$relative" ]]; then
    printf 'MISSING_REFERENCE %s\n' "$relative"
    missing=1
  fi
done < <(rg -o 'evidence/[A-Za-z0-9_.-]+' /audit-output/REVIEW.md | sort -u)
[[ $missing -eq 0 ]]

printf '%s\n' 'FINAL_MARKERS_OK'
printf '%s\n' 'SEVEN_STAGE_HEADINGS_OK'
printf '%s\n' 'EVIDENCE_REFERENCES_OK'
sha256sum /audit-output/REVIEW.md
