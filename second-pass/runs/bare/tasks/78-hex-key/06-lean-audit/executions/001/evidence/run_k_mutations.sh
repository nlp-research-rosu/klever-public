#!/usr/bin/env bash
set -euo pipefail

work=$(mktemp -d /tmp/audit-work/k-mutations.XXXXXX)
echo "work=$work"
cp /reference/k-proof/semantic.k /reference/k-proof/verification.k "$work"/
cp /audit-output/evidence/spec-false-postcondition.k "$work"/
cp /audit-output/evidence/spec-body-counterfactual.k "$work"/
cd "$work"

echo "COMMAND kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled"
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
echo "exit_code=$?"

expect_failure() {
  local spec=$1
  local module=$2
  local code

  echo "COMMAND kprove $spec --definition verification-kompiled --spec-module $module"
  set +e
  kprove "$spec" \
    --definition verification-kompiled \
    --spec-module "$module"
  code=$?
  set -e
  echo "exit_code=$code"
  if [[ $code -eq 0 ]]; then
    echo "EXPECTED nonzero exit for $spec" >&2
    return 1
  fi
}

expect_failure spec-false-postcondition.k HEX-KEY-SPEC-FALSE-POST
expect_failure spec-body-counterfactual.k HEX-KEY-SPEC-BODY-COUNTERFACTUAL

echo "all_mutations_rejected=true"
