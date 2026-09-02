#!/usr/bin/env bash
set -euo pipefail

review=/audit-output/REVIEW.md
expected=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
actual=$(tail -n 2 "$review")

[[ "$actual" == "$expected" ]]
[[ $(rg -c '^VERDICT:' "$review") -eq 1 ]]
[[ $(rg -c '^LEGITIMACY:' "$review") -eq 1 ]]

printf 'FINAL_MARKERS:\n%s\n' "$actual"
printf 'REVIEW_SHA256:\n'
sha256sum "$review"
printf 'REVIEW_LINE_COUNT:\n'
wc -l "$review"
printf 'EVIDENCE_MANIFEST:\n'
find /audit-output/evidence -maxdepth 2 -type f -printf '%p size=%s\n' | sort
