#!/usr/bin/env bash
set -euxo pipefail

diff -u \
  /tmp/audit-work/reconstruction/program.k \
  /tmp/audit-work/body-mutation/program.k || diff_status=$?
test "${diff_status}" -eq 1

cd /tmp/audit-work/body-mutation
test ! -e verification-body-mutated-kompiled
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mutated-kompiled

set +e
kprove spec.k \
  --definition verification-body-mutated-kompiled \
  --spec-module SPEC \
  > /audit-output/evidence/04-body-sensitivity-kprove.log 2>&1
mutation_status=$?
set -e
printf 'body_sensitivity_kprove_exit=%s\n' "${mutation_status}"
test "${mutation_status}" -ne 0
rg -n 'WarnStuckClaimState|\\[Error\\]|<k>|1 ~> \\.K' \
  /audit-output/evidence/04-body-sensitivity-kprove.log | head -n 80
