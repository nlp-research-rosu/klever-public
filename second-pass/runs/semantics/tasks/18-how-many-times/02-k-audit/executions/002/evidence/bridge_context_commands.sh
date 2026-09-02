#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh || exit 90

echo '$ kompile fixed-only.k --backend haskell --main-module HOW-MANY-TIMES-FIXED-ONLY --syntax-module MPY-SYNTAX --output-definition fixed-only-kompiled'
kompile fixed-only.k \
  --backend haskell \
  --main-module HOW-MANY-TIMES-FIXED-ONLY \
  --syntax-module MPY-SYNTAX \
  --output-definition fixed-only-kompiled
build_status=$?
echo "exit_status=$build_status"

echo '$ kprove spec-bad-env-bridge.k --definition verification-kompiled --spec-module HOW-MANY-TIMES-BAD-ENV-BRIDGE'
kprove spec-bad-env-bridge.k \
  --definition verification-kompiled \
  --spec-module HOW-MANY-TIMES-BAD-ENV-BRIDGE
bridge_status=$?
echo "exit_status=$bridge_status"

echo '$ kprove spec-bad-env-fixed.k --definition fixed-only-kompiled --spec-module HOW-MANY-TIMES-BAD-ENV-FIXED'
set +e
kprove spec-bad-env-fixed.k \
  --definition fixed-only-kompiled \
  --spec-module HOW-MANY-TIMES-BAD-ENV-FIXED \
  2>&1 | tee /audit-output/evidence/bridge-fixed-only.raw.log
fixed_status=${PIPESTATUS[0]}
set -e
echo "exit_status=$fixed_status (expected nonzero: fixed execution cannot resolve len in the missing scope chain)"

echo '$ rg -n "WarnStuckClaimState|#look|cannot be rewritten further" /audit-output/evidence/bridge-fixed-only.raw.log'
rg -n \
  'WarnStuckClaimState|#look|cannot be rewritten further' \
  /audit-output/evidence/bridge-fixed-only.raw.log
residual_status=$?
echo "exit_status=$residual_status"

if (( build_status != 0 || bridge_status != 0 || fixed_status == 0 || residual_status != 0 )); then
  exit 1
fi
exit 0
