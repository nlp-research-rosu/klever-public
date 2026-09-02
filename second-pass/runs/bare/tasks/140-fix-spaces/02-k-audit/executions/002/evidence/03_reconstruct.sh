#!/usr/bin/env bash
set -uo pipefail
set -x

kompile --version
kompile_version_status=$?
kprove --version
kprove_version_status=$?
krun --version
krun_version_status=$?

kompile --backend haskell \
  /tmp/audit-work/candidate/semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/semantic-kompiled
semantic_build_status=$?

kompile --backend haskell \
  /tmp/audit-work/candidate/verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-kompiled
verification_build_status=$?

if (( verification_build_status == 0 )); then
  kprove /tmp/audit-work/candidate/spec.k \
    --definition /tmp/audit-work/build/verification-kompiled \
    --spec-module SPEC
  positive_proof_status=$?
else
  positive_proof_status=125
fi

set +x
printf 'kompile_version_exit=%s\n' "$kompile_version_status"
printf 'kprove_version_exit=%s\n' "$kprove_version_status"
printf 'krun_version_exit=%s\n' "$krun_version_status"
printf 'semantic_build_exit=%s\n' "$semantic_build_status"
printf 'verification_build_exit=%s\n' "$verification_build_status"
printf 'positive_proof_exit=%s\n' "$positive_proof_status"

if (( kompile_version_status != 0 ||
      kprove_version_status != 0 ||
      krun_version_status != 0 ||
      semantic_build_status != 0 ||
      verification_build_status != 0 ||
      positive_proof_status != 0 )); then
  exit 1
fi
