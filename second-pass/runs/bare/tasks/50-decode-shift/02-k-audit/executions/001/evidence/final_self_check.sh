#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md
scratch=/tmp/audit-work/50-decode-shift/candidate-src
status=0

expected_tail=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
actual_tail=$(tail -n 2 "$review")
if [[ "$actual_tail" == "$expected_tail" ]]; then
  printf 'REVIEW_MARKERS_OK\n'
else
  printf 'REVIEW_MARKERS_BAD\n%s\n' "$actual_tail"
  status=1
fi

for name in solution.py solution.mpy semantic.k verification.k spec.k; do
  cmp -s "/candidate/$name" "$scratch/$name"
  cmp_status=$?
  printf 'SCRATCH_SOURCE_CMP\t%s\t%s\n' "$name" "$cmp_status"
  (( cmp_status == 0 )) || status=1
done

for log in \
  06_kompile_llvm.log \
  07_kompile_haskell.log \
  11_kprove_code_inverse.log \
  12_kprove_loop_correct.log \
  15_kprove_loop_and_program.log \
  16_kprove_aggregate.log \
  21_vacuity_dry_run.log; do
  if tail -n 3 "/audit-output/evidence/$log" | rg -q 'EXIT_STATUS: 0'; then
    printf 'EXPECTED_ZERO_OK\t%s\n' "$log"
  else
    printf 'EXPECTED_ZERO_BAD\t%s\n' "$log"
    status=1
  fi
done

if tail -n 3 /audit-output/evidence/22_vacuity_kprove_expected_failure.log |
    rg -q 'EXIT_STATUS: 1'; then
  printf 'EXPECTED_VACUITY_FAILURE_OK\n'
else
  printf 'EXPECTED_VACUITY_FAILURE_BAD\n'
  status=1
fi

symlink_count=$(find /audit-output/evidence -type l | wc -l)
printf 'EVIDENCE_SYMLINK_COUNT\t%s\n' "$symlink_count"
(( symlink_count == 0 )) || status=1

printf 'FINAL_SELF_CHECK_STATUS\t%s\n' "$status"
exit "$status"
