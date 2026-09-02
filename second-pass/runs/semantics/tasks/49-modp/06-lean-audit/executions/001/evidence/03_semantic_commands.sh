#!/usr/bin/env bash
set -eu

audit_stage1_tmp="$(mktemp -d /tmp/audit-work/stage1-semantic.XXXXXX)"
cp -a /reference/k-proof/. "${audit_stage1_tmp}/"
printf 'AUDIT_STAGE1_TMP=%s\n' "${audit_stage1_tmp}"

printf '%s\n' '$ kompile supplied semantics with LLVM backend'
(
  cd "${audit_stage1_tmp}"
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-kompiled \
    -w none
)

printf '%s\n' '$ krun original concrete-tests.mpy'
(
  cd "${audit_stage1_tmp}"
  krun concrete-tests.mpy --definition runtime-kompiled
)

printf '%s\n' '$ krun independently authored boundary/adversarial examples'
(
  cd "${audit_stage1_tmp}"
  krun /audit-output/evidence/semantic-positive.mpy \
    --definition runtime-kompiled
)

printf '%s\n' '$ krun deliberately false counterfactual expected value (semantic exit-code must be 1)'
set +e
(
  cd "${audit_stage1_tmp}"
  krun /audit-output/evidence/semantic-counterfactual.mpy \
    --definition runtime-kompiled
)
counterfactual_status=$?
set -e
printf 'counterfactual_krun_exit=%s\n' "${counterfactual_status}"
if [ "${counterfactual_status}" -eq 0 ]; then
  printf '%s\n' 'ERROR: deliberately false counterfactual was accepted'
  exit 1
fi

printf '%s\n' '$ kompile frozen verification.k with Haskell backend'
(
  cd "${audit_stage1_tmp}"
  kompile verification.k \
    --backend haskell \
    --main-module MODP-VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-kompiled \
    -w none
)

printf '%s\n' '$ kprove frozen spec.k'
(
  cd "${audit_stage1_tmp}"
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module MODP-SPEC \
    -w none
)
