#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/75-is-multiply-prime/body-mutation

kompile definition.k \
  --backend haskell \
  --main-module DEFINITION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutation-kompiled

set +e
kprove spec.k \
  --definition body-mutation-kompiled \
  --spec-module SPEC 2>&1 | tee body-mutation-proof-output.txt
body_kprove_status=${PIPESTATUS[0]}
set -e

echo "kprove_exit=${body_kprove_status}"
test "${body_kprove_status}" -ne 0
rg -n 'WarnStuckClaimState|implication check.*failed|cannot be rewritten further' \
  body-mutation-proof-output.txt
