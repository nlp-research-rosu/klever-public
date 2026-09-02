#!/usr/bin/env bash
set -euo pipefail
set -x

audit_project=/tmp/audit-work/lean-proof-audit
cd "${audit_project}"
lake env lean AxiomAudit.lean
lake env lean OperationalBridgeAudit.lean
lake env lean CounterfactualAudit.lean
