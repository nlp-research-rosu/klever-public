#!/usr/bin/env bash
set -eu
set -o pipefail

review=/audit-output/REVIEW.md
evidence=/audit-output/evidence

printf '$ tail -n 2 %s\n' "$review"
tail -n 2 "$review"
test "$(tail -n 2 "$review")" = $'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
test "$(grep -c '^VERDICT:' "$review")" -eq 1
test "$(grep -c '^LEGITIMACY:' "$review")" -eq 1

for stage in 1 2 3 4 5 6 7; do
  grep -q "^## ${stage}\\." "$review"
done

for proof in inner outer entry; do
  grep -q '^#Top$' "$evidence/03_kprove_${proof}.log"
  grep -q '^\[exit 0\]$' "$evidence/03_kprove_${proof}.log"
done

grep -q 'WarnStuckClaimState' "$evidence/05_false_n5.log"
grep -q '^\[exit 1\]$' "$evidence/05_false_n5.log"
grep -q 'WarnStuckClaimState' "$evidence/04_body_sensitivity.log"
grep -q '^\[exit 1\]$' "$evidence/04_body_sensitivity.log"

test -z "$(find "$evidence" -type l -print)"
diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics

echo "review structure, proof logs, negative probes, and final markers: OK"
