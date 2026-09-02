#!/usr/bin/env bash
set -u

work=/tmp/audit-work/37-sort-even-audit/body-mutation
evidence=/audit-output/evidence
build_log=$evidence/stage4-body-mutation-build.log
proof_log=$evidence/stage4-body-mutation-proof.log

cd "$work" || exit 1
if test -e verification-mutated-kompiled; then
  echo 'refusing to reuse an existing mutated definition'
  exit 2
fi

echo '$ diff -u /tmp/audit-work/37-sort-even-audit/source/verification.k /tmp/audit-work/37-sort-even-audit/body-mutation/verification.k'
diff -u /tmp/audit-work/37-sort-even-audit/source/verification.k verification.k || true

(
  echo '$ kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX -I . --output-definition verification-mutated-kompiled'
  kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    -I . \
    --output-definition verification-mutated-kompiled
  command_status=$?
  echo "exit=$command_status"
  exit "$command_status"
) > "$build_log" 2>&1
build_status=$?
echo "body_mutation_build_exit=$build_status"
if test "$build_status" -ne 0; then
  exit 1
fi

(
  echo '$ kprove spec.k --definition verification-mutated-kompiled --spec-module SPEC --claims SPEC.loop-correct --output pretty'
  kprove spec.k \
    --definition verification-mutated-kompiled \
    --spec-module SPEC \
    --claims SPEC.loop-correct \
    --output pretty
  command_status=$?
  echo "exit=$command_status"
  exit "$command_status"
) > "$proof_log" 2>&1
proof_status=$?
echo "body_mutation_proof_exit=$proof_status"

if test "$proof_status" -eq 0; then
  echo 'ERROR: materially changed loop body still proved the original invariant'
  exit 1
fi
if rg -q 'WarnStuckClaimState|implication check between the conditions has failed' "$proof_log"; then
  echo 'body_sensitivity_residual=yes'
  exit 0
fi
echo 'ERROR: body mutation did not produce a semantic residual'
exit 1
