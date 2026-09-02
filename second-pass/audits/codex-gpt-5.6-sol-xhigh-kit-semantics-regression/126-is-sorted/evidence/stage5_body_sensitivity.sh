#!/usr/bin/env bash
set -uo pipefail
set -x

mut=/tmp/audit-work/body-mutation
raw=/tmp/audit-work/stage5-body-raw
mkdir -p "$raw"
overall=0

printf '%s\n' 'MUTATION DIFF'
diff -u \
  /tmp/audit-work/candidate-src/verification.k \
  "$mut/verification.k"
diff_status=$?
printf 'mutation_diff_status=%s (1 means files differ as intended)\n' "$diff_status"
if (( diff_status != 1 )); then
  overall=1
fi

kompile --backend haskell "$mut/verification.k" \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition "$mut/audit-body-mutated-kompiled" \
  > "$raw/kompile.log" 2>&1
build_status=$?
printf '%s\n' \
  'COMMAND: kompile --backend haskell /tmp/audit-work/body-mutation/verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/body-mutation/audit-body-mutated-kompiled'
printf 'EXIT[body-mutation-build]=%s\n' "$build_status"
sed -n '1,160p' "$raw/kompile.log"
if (( build_status != 0 )); then
  overall=1
fi

kprove "$mut/spec.k" \
  --definition "$mut/audit-body-mutated-kompiled" \
  --spec-module SPEC \
  > "$raw/kprove.log" 2>&1
prove_status=$?
printf '%s\n' \
  'COMMAND: kprove /tmp/audit-work/body-mutation/spec.k --definition /tmp/audit-work/body-mutation/audit-body-mutated-kompiled --spec-module SPEC'
printf 'EXIT[body-mutation-proof]=%s (nonzero expected)\n' "$prove_status"
sed -n '1,220p' "$raw/kprove.log"
if (( prove_status == 0 )); then
  overall=1
fi
if ! grep -q 'WarnStuckClaimState' "$raw/kprove.log"; then
  printf '%s\n' 'ERROR: expected semantic stuck-claim residual was absent'
  overall=1
fi

printf 'STAGE5_BODY_SENSITIVITY_OVERALL=%s\n' "$overall"
exit "$overall"
