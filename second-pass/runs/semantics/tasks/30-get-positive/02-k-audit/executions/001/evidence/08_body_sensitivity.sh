#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive
failed=0

printf '$ kompile %s/verification-body-mut.k --backend haskell --main-module VERIFICATION-BODY-MUT --syntax-module VERIFICATION-BODY-MUT --output-definition %s/body-mut-kompiled\n' \
  "$work" "$work"
kompile "$work/verification-body-mut.k" \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUT \
  --syntax-module VERIFICATION-BODY-MUT \
  --output-definition "$work/body-mut-kompiled"
build_status=$?
printf '[exit %d]\n' "$build_status"
if test "$build_status" -ne 0; then
  failed=1
fi

printf '\n$ kprove %s/body-mut-spec.k --definition %s/body-mut-kompiled --spec-module BODY-MUT-SPEC --smt-timeout 10000\n' \
  "$work" "$work"
kprove "$work/body-mut-spec.k" \
  --definition "$work/body-mut-kompiled" \
  --spec-module BODY-MUT-SPEC \
  --smt-timeout 10000 \
  > /audit-output/evidence/08_body_sensitivity.raw.log 2>&1
proof_status=$?
sed -n '1,300p' /audit-output/evidence/08_body_sensitivity.raw.log
printf '[exit %d]\n' "$proof_status"

if test "$proof_status" -eq 0; then
  printf 'ERROR: the materially changed body unexpectedly proved the original summary\n'
  failed=1
fi
if ! rg -q 'WarnStuckClaimState' /audit-output/evidence/08_body_sensitivity.raw.log; then
  printf 'ERROR: expected stuck-claim diagnostic was absent\n'
  failed=1
fi

exit "$failed"
