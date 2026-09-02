#!/usr/bin/env bash
set -euxo pipefail

export PYTHONPATH=/reference
python /audit-output/evidence/02_inventory_audit.py
sed -n '1,260p' /reference/lemma-discovery.json
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/semantic.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/prove.sh
