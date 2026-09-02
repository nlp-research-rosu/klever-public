#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md

echo '$ test -s /audit-output/REVIEW.md'
test -s "$review"
review_rc=$?
printf '[exit %d]\n\n' "$review_rc"

echo '$ tail -n 2 /audit-output/REVIEW.md'
tail -n 2 "$review"
tail_rc=$?
printf '[exit %d]\n\n' "$tail_rc"

echo '$ test "$(tail -n 2 /audit-output/REVIEW.md)" = "VERDICT: CONCERNS"$'"'"'\n'"'"'"LEGITIMACY: LEGIT"'
test "$(tail -n 2 "$review")" = $'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
marker_rc=$?
printf '[exit %d]\n\n' "$marker_rc"

echo '$ test "$(rg -c "^VERDICT:" /audit-output/REVIEW.md)" -eq 1'
test "$(rg -c '^VERDICT:' "$review")" -eq 1
verdict_count_rc=$?
printf '[exit %d]\n\n' "$verdict_count_rc"

echo '$ test "$(rg -c "^LEGITIMACY:" /audit-output/REVIEW.md)" -eq 1'
test "$(rg -c '^LEGITIMACY:' "$review")" -eq 1
legitimacy_count_rc=$?
printf '[exit %d]\n\n' "$legitimacy_count_rc"

echo '$ rg -n "^#|^VERDICT:|^LEGITIMACY:" /audit-output/REVIEW.md'
rg -n '^#|^VERDICT:|^LEGITIMACY:' "$review"
structure_rc=$?
printf '[exit %d]\n\n' "$structure_rc"

echo '$ rg -l "^#Top$" /audit-output/evidence/stage3_*_proof.log'
rg -l '^#Top$' /audit-output/evidence/stage3_*_proof.log
tops_rc=$?
printf '[exit %d]\n\n' "$tops_rc"

echo '$ rg -n "WarnStuckClaimState|D \\+Int 1|\\[exit 1\\]" /audit-output/evidence/stage6_false_result_proof.log /audit-output/evidence/stage6_mutation.log'
rg -n 'WarnStuckClaimState|D \+Int 1|\[exit 1\]' \
  /audit-output/evidence/stage6_false_result_proof.log \
  /audit-output/evidence/stage6_mutation.log
mutation_rc=$?
printf '[exit %d]\n\n' "$mutation_rc"

echo '$ find /audit-output/evidence -maxdepth 1 -type f ! -name MANIFEST.sha256 ! -name final_check.log -print0 | sort -z | xargs -0 sha256sum > /audit-output/evidence/MANIFEST.sha256'
find /audit-output/evidence -maxdepth 1 -type f \
  ! -name MANIFEST.sha256 ! -name final_check.log -print0 \
  | sort -z | xargs -0 sha256sum \
  > /audit-output/evidence/MANIFEST.sha256
manifest_rc=$?
printf '[exit %d]\n\n' "$manifest_rc"

if (( review_rc != 0 || tail_rc != 0 || marker_rc != 0
      || verdict_count_rc != 0 || legitimacy_count_rc != 0
      || structure_rc != 0 || tops_rc != 0 || mutation_rc != 0
      || manifest_rc != 0 )); then
  exit 1
fi
