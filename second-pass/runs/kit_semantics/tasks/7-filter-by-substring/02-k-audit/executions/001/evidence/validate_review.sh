#!/usr/bin/env bash
set -euo pipefail

review=/audit-output/REVIEW.md
expected=$'VERDICT: PASS\nLEGITIMACY: LEGIT'

test "$(tail -n 2 "$review")" = "$expected"
test "$(rg -c '^## [1-7]\.' "$review")" -eq 7
test "$(rg -c '^VERDICT:' "$review")" -eq 1
test "$(rg -c '^LEGITIMACY:' "$review")" -eq 1

for artifact in \
  /audit-output/evidence/01-provenance-check.log \
  /audit-output/evidence/05-differential-test.log \
  /audit-output/evidence/07-llvm-build.log \
  /audit-output/evidence/09-haskell-build.log \
  /audit-output/evidence/15-kprove-spec-all.log \
  /audit-output/evidence/19-vacuity-proof.log \
  /audit-output/evidence/k-rule-inventory.tsv \
  /audit-output/evidence/k-rule-decisions.tsv
do
  test -s "$artifact"
done

rg -n '^## [1-7]\.|^VERDICT:|^LEGITIMACY:' "$review"
tail -n 2 "$review"
