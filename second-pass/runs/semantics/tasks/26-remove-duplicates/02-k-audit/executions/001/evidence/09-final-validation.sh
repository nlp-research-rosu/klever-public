#!/usr/bin/env bash
set -euo pipefail

review=/audit-output/REVIEW.md
evidence=/audit-output/evidence

diff --no-dereference -r \
  /reference/reference-semantics \
  /candidate/reference-semantics
cmp -s /reference/prompt.py /candidate/prompt.py
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
cmp -s \
  /tmp/audit-work/26-remove-duplicates/candidate/spec-vacuity.k \
  "$evidence/08-spec-vacuity.k"

for log in \
  "$evidence/05-kprove-loop-invariant.log" \
  "$evidence/05-kprove-entry-empty.log" \
  "$evidence/05-kprove-entry-keep.log" \
  "$evidence/05-kprove-entry-drop.log"
do
  tr -d '\r' < "$log" | grep -q '#Top'
  tr -d '\r' < "$log" | grep -q 'EXIT_STATUS=0'
done

tr -d '\r' < "$evidence/08-vacuity-build-and-proof.log" |
  grep -q 'DRY_RUN_EXIT_STATUS=0'
tr -d '\r' < "$evidence/08-vacuity-build-and-proof.log" |
  grep -q 'WarnStuckClaimState'
tr -d '\r' < "$evidence/08-vacuity-build-and-proof.log" |
  grep -q 'KPROVE_EXIT_STATUS=1'

if grep -q 'PENDING_FINAL_LOG' "$review" "$evidence/COMMANDS.md"; then
  echo "pending marker remains" >&2
  exit 1
fi

test "$(tail -n 2 "$review" | sed -n '1p')" = 'VERDICT: CONCERNS'
test "$(tail -n 2 "$review" | sed -n '2p')" = 'LEGITIMACY: LEGIT'
test "$(grep -c '^VERDICT:' "$review")" -eq 1
test "$(grep -c '^LEGITIMACY:' "$review")" -eq 1

while IFS= read -r target; do
  test -e "/audit-output/$target"
done < <(
  grep -oE '\]\(evidence/[^)]+\)' "$review" |
    sed -e 's/^](//' -e 's/)$//' |
    sort -u
)

echo "semantics_diff=0"
echo "trusted_prompt_cmp=0"
echo "trusted_translator_cmp=0"
echo "positive_claim_logs=4/4"
echo "false_mutation=build_0_proof_1_expected_residual"
echo "review_links=all_exist"
echo "review_terminator=exact"
echo "RESULT=PASS"
