#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words
cp /audit-output/evidence/11_false_program_claims.k false-program-claims.k
cp /audit-output/evidence/11_false_program_claims_no_bridges.k false-program-claims-no-bridges.k

echo '$ kprove false-program-claims.k --definition audit-verification-kompiled --spec-module FALSE-PROGRAM-CLAIMS'
kprove false-program-claims.k \
  --definition audit-verification-kompiled \
  --spec-module FALSE-PROGRAM-CLAIMS
echo "extended_false_program_claims_exit=$?"

for label in empty-forced-whitespace space-forced-comma comma-forced-count; do
  echo "$ kprove false-program-claims-no-bridges.k --definition audit-no-bridges-kompiled --spec-module FALSE-PROGRAM-CLAIMS-NO-BRIDGES --claims FALSE-PROGRAM-CLAIMS-NO-BRIDGES.$label"
  kprove false-program-claims-no-bridges.k \
    --definition audit-no-bridges-kompiled \
    --spec-module FALSE-PROGRAM-CLAIMS-NO-BRIDGES \
    --claims "FALSE-PROGRAM-CLAIMS-NO-BRIDGES.$label"
  echo "${label}_no_bridges_exit=$?"
done
