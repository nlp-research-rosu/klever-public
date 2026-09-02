#!/usr/bin/env bash
set -euo pipefail

cd /audit-output

printf '$ test -s /audit-output/REVIEW.md\n'
test -s /audit-output/REVIEW.md
printf '[exit 0]\n'

printf '\n$ tail -n 2 /audit-output/REVIEW.md\n'
tail -n 2 /audit-output/REVIEW.md

expected='VERDICT: CONCERNS
LEGITIMACY: LEGIT'
test "$(tail -n 2 /audit-output/REVIEW.md)" = "$expected"
printf '[marker-check exit 0]\n'

printf '\n$ rg -c "^## [1-7]\\." /audit-output/REVIEW.md\n'
stage_count=$(rg -c '^## [1-7]\.' /audit-output/REVIEW.md)
printf '%s\n' "$stage_count"
test "$stage_count" -eq 7
printf '[stage-check exit 0]\n'

missing=0
while IFS= read -r relative_path; do
  if [ ! -e "/audit-output/$relative_path" ]; then
    printf 'missing link target: %s\n' "$relative_path"
    missing=1
  fi
done < <(rg -o '\(evidence/[^)]+' /audit-output/REVIEW.md | sed 's/^(//')
test "$missing" -eq 0
printf '[evidence-link-check exit 0]\n'

sha256sum /audit-output/REVIEW.md
