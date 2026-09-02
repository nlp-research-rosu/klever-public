#!/usr/bin/env bash
set -euo pipefail
set -o xtrace
export PATH="/home/agent/.nix-profile/bin:$PATH"
scratch=/tmp/audit-work/54-same-chars
cd "$scratch"
cp /audit-output/evidence/audit-spec-vacuity.k audit-spec-vacuity.k
cp /audit-output/evidence/audit-spec-body-sensitivity.k audit-spec-body-sensitivity.k

set +e
kprove audit-spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY \
  --dry-run > audit-vacuity-dry-run.out 2>&1
vacuity_dry_status=$?
kprove audit-spec-body-sensitivity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-BODY-SENSITIVITY \
  --dry-run > audit-body-dry-run.out 2>&1
body_dry_status=$?
set -e

wc -c audit-vacuity-dry-run.out audit-body-dry-run.out
sed -n '1,8p' audit-vacuity-dry-run.out
sed -n '1,8p' audit-body-dry-run.out

set +e
kprove audit-spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY 2>&1 | tee audit-vacuity-proof.out
vacuity_status=${PIPESTATUS[0]}
kprove audit-spec-body-sensitivity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-BODY-SENSITIVITY 2>&1 | tee audit-body-proof.out
body_status=${PIPESTATUS[0]}
set -e

rg -F 'WarnStuckClaimState' audit-vacuity-proof.out
rg -F '"result" |-> true' audit-vacuity-proof.out
rg -F 'WarnStuckClaimState' audit-body-proof.out
rg -F '"result" |-> true' audit-body-proof.out

printf 'VACUITY_DRY_RUN_EXIT_STATUS=%s\n' "$vacuity_dry_status"
printf 'BODY_DRY_RUN_EXIT_STATUS=%s\n' "$body_dry_status"
printf 'VACUITY_PROOF_EXIT_STATUS=%s\n' "$vacuity_status"
printf 'BODY_PROOF_EXIT_STATUS=%s\n' "$body_status"
if (( vacuity_dry_status != 0 || body_dry_status != 0 )); then
  exit 1
fi
if (( vacuity_status == 0 || body_status == 0 )); then
  exit 1
fi
printf 'EXIT_STATUS=0\n'
