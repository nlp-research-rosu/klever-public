#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/body-mutation
sha256sum verification.k
rg -n -C 2 'CmpOp' verification.k
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutated-kompiled

set +e
proof_output="$(kprove spec.k \
  --definition body-mutated-kompiled \
  --spec-module SPEC \
  --claims SPEC.example-true 2>&1)"
proof_exit=$?
set -e
printf '%s\n' "$proof_output"
printf 'body_mutation_kprove_exit=%s\n' "$proof_exit"
test "$proof_exit" -ne 0
grep -Fq 'WarnStuckClaimState' <<<"$proof_output"
grep -Fq "doesn't unify with the destination's term" <<<"$proof_output"
grep -Fq 'result ( boolVal ( false ) )' <<<"$proof_output"
