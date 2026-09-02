#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/114-minSubArraySum

printf '$ wc -l verification-base-kompiled/allRules.txt verification-kompiled/allRules.txt\n'
wc -l \
  "$scratch/verification-base-kompiled/allRules.txt" \
  "$scratch/verification-kompiled/allRules.txt"
printf '[exit %d]\n' "$?"

printf '$ diff -u verification-base-kompiled/allRules.txt verification-kompiled/allRules.txt\n'
diff -u \
  "$scratch/verification-base-kompiled/allRules.txt" \
  "$scratch/verification-kompiled/allRules.txt"
status=$?
printf '[exit %d; one added rule is expected]\n' "$status"
