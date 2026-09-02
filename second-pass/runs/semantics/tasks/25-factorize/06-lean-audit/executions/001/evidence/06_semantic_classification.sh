#!/usr/bin/env bash
set -uo pipefail

echo '$ nl -ba /reference/k-proof/reference-semantics/semantics/controls.k | sed -n "8,31p;46,55p;62,108p"'
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k \
  | sed -n '8,31p;46,55p;62,108p'

echo '$ nl -ba /reference/k-proof/reference-semantics/semantics/int.k | sed -n "7,28p"'
nl -ba /reference/k-proof/reference-semantics/semantics/int.k \
  | sed -n '7,28p'

echo '$ nl -ba /reference/k-proof/reference-semantics/semantics/list.k | sed -n "12,28p;52,55p"'
nl -ba /reference/k-proof/reference-semantics/semantics/list.k \
  | sed -n '12,28p;52,55p'

echo '$ nl -ba /reference/k-proof/reference-semantics/semantics/functions.k | sed -n "13,20p;62,91p"'
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k \
  | sed -n '13,20p;62,91p'

echo '$ nl -ba /reference/k-proof/reference-semantics/semantics/call.k | sed -n "15,24p;52,75p"'
nl -ba /reference/k-proof/reference-semantics/semantics/call.k \
  | sed -n '15,24p;52,75p'

echo '$ nl -ba /reference/k-proof/reference-semantics/semantics/core.k | sed -n "62,70p;117,135p"'
nl -ba /reference/k-proof/reference-semantics/semantics/core.k \
  | sed -n '62,70p;117,135p'

echo '$ PYTHONPATH=/reference python3 /audit-output/evidence/06_semantic_classification.py'
PYTHONPATH=/reference python3 /audit-output/evidence/06_semantic_classification.py
