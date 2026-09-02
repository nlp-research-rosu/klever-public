#!/usr/bin/env bash
set -u
set -o pipefail
trap 'status=$?; printf "SCRIPT_EXIT=%s\n" "$status"' EXIT
set -x

audit_work=/tmp/audit-work/audit149
PYTHONDONTWRITEBYTECODE=1 python3 /audit-output/evidence/claim_witnesses.py \
  "$audit_work/trusted-canonical.py" \
  "$audit_work/solution.py"
