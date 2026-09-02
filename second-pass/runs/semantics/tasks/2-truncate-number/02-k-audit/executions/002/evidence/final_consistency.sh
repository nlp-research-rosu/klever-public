#!/usr/bin/env bash
set -uo pipefail

review=/audit-output/REVIEW.md
status=0

echo "Final marker check:"
actual_tail=$(tail -n 2 "$review")
expected_tail=$'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
printf '%s\n' "$actual_tail"
if [[ "$actual_tail" != "$expected_tail" ]]; then
  status=1
fi

echo
echo "Required decisive evidence:"
required=(
  evidence/stage1-integrity.log
  evidence/stage1-generation-record-inspection.log
  evidence/stage2-regeneration.log
  evidence/stage2-differential.log
  evidence/stage3-kompile-llvm.log
  evidence/stage3-krun-candidate-tests.log
  evidence/stage3-kompile-haskell.log
  evidence/stage3-kprove-positive.log
  evidence/stage4-program-pinning.log
  evidence/rule-inventory.md
  evidence/stage5-body-mutation-kprove.log
  evidence/stage5-k-float-normal-suite-final.log
  evidence/stage5-float-subnormal-exact-assert.log
  evidence/spec-vacuity.k
  evidence/stage6-vacuity-dry-run.log
  evidence/stage6-vacuity-kprove.log
)
for relative in "${required[@]}"; do
  path=/audit-output/$relative
  if [[ -f "$path" && ! -L "$path" ]]; then
    printf 'OK %s\n' "$relative"
  else
    printf 'FAIL %s\n' "$relative"
    status=1
  fi
done

echo
echo "Decisive command exit markers:"
for relative in \
  evidence/stage1-integrity.log \
  evidence/stage2-regeneration.log \
  evidence/stage2-differential.log \
  evidence/stage3-kompile-llvm.log \
  evidence/stage3-krun-candidate-tests.log \
  evidence/stage3-kompile-haskell.log \
  evidence/stage3-kprove-positive.log \
  evidence/stage5-body-mutation-kompile.log \
  evidence/stage5-body-mutation-kprove.log \
  evidence/stage6-vacuity-dry-run.log \
  evidence/stage6-vacuity-kprove.log
do
  printf '%s: ' "$relative"
  tail -n 1 "/audit-output/$relative"
done

echo
echo "Positive/negative semantic signals:"
rg -n '^#Top|WarnStuckClaimState|floatMod \\( N , 1\\.0 \\)|addF \\( N , 1\\.0 \\)' \
  /audit-output/evidence/stage3-kprove-positive.log \
  /audit-output/evidence/stage5-body-mutation-kprove.log \
  /audit-output/evidence/stage6-vacuity-kprove.log

echo
echo "FINAL_CONSISTENCY_EXIT=$status"
exit "$status"
