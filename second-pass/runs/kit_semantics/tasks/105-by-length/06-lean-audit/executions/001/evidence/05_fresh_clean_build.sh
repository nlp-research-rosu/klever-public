#!/usr/bin/env bash
set -euo pipefail
set -x

audit_project=/tmp/audit-work/lean-proof-audit
test ! -e "${audit_project}"
mkdir -p "${audit_project}"
cp -a /candidate/Proof.lean "${audit_project}/Proof.lean"
cp -a /candidate/lake-manifest.json "${audit_project}/lake-manifest.json"
cp -a /candidate/lakefile.lean "${audit_project}/lakefile.lean"
cp -a /candidate/lean-toolchain "${audit_project}/lean-toolchain"
cp -a /reference/klean-generation/generated "${audit_project}/Base"
cp -a /audit-output/evidence/AxiomAudit.lean "${audit_project}/AxiomAudit.lean"
cp -a /audit-output/evidence/OperationalBridgeAudit.lean \
  "${audit_project}/OperationalBridgeAudit.lean"
cp -a /audit-output/evidence/CounterfactualAudit.lean \
  "${audit_project}/CounterfactualAudit.lean"

cd "${audit_project}"
lake clean
lake build
