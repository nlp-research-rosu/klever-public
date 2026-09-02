#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md
status=0

printf '$ tail -n 2 %s\n' "$review"
tail -n 2 "$review"
test "$(tail -n 2 "$review")" = $'VERDICT: CONCERNS\nLEGITIMACY: LEGIT' || status=1

printf '\n$ rg -n "^## [1-7]\\." %s\n' "$review"
rg -n '^## [1-7]\.' "$review" || status=1

printf '\nPositive proof signals:\n'
for log in \
  /audit-output/evidence/03_positive_all.log \
  /audit-output/evidence/03_positive_len_{0,1,2,3,4,5,6,7}.log
do
  top_count=$(rg -c '^#Top$' "$log" || true)
  exit_count=$(rg -c '^\[exit 0\]$' "$log" || true)
  printf '%s top=%s exit0=%s\n' "$(basename "$log")" "$top_count" "$exit_count"
  test "$top_count" = 1 && test "$exit_count" = 1 || status=1
done

printf '\nNegative proof signals:\n'
negative=/audit-output/evidence/06_false_result_proof.log
stuck_count=$(rg -c 'WarnStuckClaimState' "$negative" || true)
top_count=$(rg -c '^#Top$' "$negative" || true)
exit_count=$(rg -c '^\[exit 1\]$' "$negative" || true)
printf '%s stuck=%s top=%s exit1=%s\n' \
  "$(basename "$negative")" "$stuck_count" "$top_count" "$exit_count"
test "$stuck_count" = 1 && test -z "$top_count" && test "$exit_count" = 1 \
  || status=1

printf '\n$ bash -n reviewer shell scripts\n'
for script in /audit-output/evidence/*.sh
do
  bash -n "$script" || status=1
done

printf '\n$ sha256sum REVIEW.md and reviewer-authored scripts\n'
sha256sum "$review" /audit-output/evidence/*.sh /audit-output/evidence/*.py

printf '\n[exit %d]\n' "$status"
exit "$status"
