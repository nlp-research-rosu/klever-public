#!/usr/bin/env bash
set -u

cd /tmp/audit-work/body-mutation || exit 90

echo '$ diff -u /candidate/verification.k verification.k'
diff -u /candidate/verification.k verification.k
diff_status=$?
echo "exit_status=$diff_status (expected 1: deliberate body mutation)"

echo '$ krun mutated-pass.mpy --definition /tmp/audit-work/fresh/runtime-kompiled'
krun mutated-pass.mpy \
  --definition /tmp/audit-work/fresh/runtime-kompiled
pass_runtime_status=$?
echo "exit_status=$pass_runtime_status"

echo '$ krun mutated-false-post.mpy --definition /tmp/audit-work/fresh/runtime-kompiled'
krun mutated-false-post.mpy \
  --definition /tmp/audit-work/fresh/runtime-kompiled
false_runtime_status=$?
echo "exit_status=$false_runtime_status (expected 1: fixed execution returns 999, not 1)"

echo '$ kompile verification.k --backend haskell --main-module HOW-MANY-TIMES-VERIFICATION --syntax-module MPY-SYNTAX --output-definition body-mutation-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module HOW-MANY-TIMES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutation-kompiled
build_status=$?
echo "exit_status=$build_status"

echo '$ kprove spec.k --definition body-mutation-kompiled --spec-module HOW-MANY-TIMES-SPEC'
kprove spec.k \
  --definition body-mutation-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC
proof_status=$?
echo "exit_status=$proof_status (UNSOUND if #Top: changed body returns 999 but claim still says overlapCount)"

if (( pass_runtime_status != 0 || false_runtime_status == 0 || build_status != 0 || proof_status != 0 )); then
  exit 1
fi
exit 0
