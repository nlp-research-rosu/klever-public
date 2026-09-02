#!/usr/bin/env bash
set -uo pipefail

review=/audit-output/REVIEW.md
expected_tail=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'

printf 'COMMAND: verify seven numbered stage headings\n'
for stage in 1 2 3 4 5 6 7; do
  rg -q "^## ${stage}\\." "$review" || exit 1
done
printf 'EXIT_STATUS: 0\n\n'

printf 'COMMAND: verify exact final markers and no later content\n'
actual_tail=$(tail -n 2 "$review")
[[ "$actual_tail" == "$expected_tail" ]]
status=$?
printf 'EXIT_STATUS: %d\n\n' "$status"
(( status == 0 )) || exit "$status"

printf 'COMMAND: verify positive proof logs contain #Top and exit 0\n'
for log in \
  /audit-output/evidence/stage3_prove_original_all.log \
  /audit-output/evidence/stage3_prove_universal.log \
  /audit-output/evidence/stage3_prove_example-increasing.log \
  /audit-output/evidence/stage3_prove_example-nonmonotonic.log \
  /audit-output/evidence/stage3_prove_example-decreasing.log
do
  rg -q '^#Top$' "$log" || exit 1
  rg -q '^EXIT_STATUS: 0$' "$log" || exit 1
  printf 'OK %s\n' "$log"
done
printf 'EXIT_STATUS: 0\n\n'

printf 'COMMAND: verify mutation built and failed for expected result residual\n'
rg -q '^EXIT_STATUS: 0$' /audit-output/evidence/stage6_mutation_dry_run.log || exit 1
rg -q 'WarnStuckClaimState' /audit-output/evidence/stage6_mutation_proof.log || exit 1
rg -Fq 'boolVal ( true )' /audit-output/evidence/stage6_mutation_proof.log || exit 1
rg -q '^EXIT_STATUS: 1$' /audit-output/evidence/stage6_mutation_proof.log || exit 1
printf 'EXIT_STATUS: 0\n\n'

printf 'COMMAND: list reviewer evidence sizes (bounded evidence check)\n'
find /audit-output/evidence -maxdepth 1 -type f -printf '%s %f\n' | sort -n
status=$?
printf 'EXIT_STATUS: %d\n' "$status"
exit "$status"
