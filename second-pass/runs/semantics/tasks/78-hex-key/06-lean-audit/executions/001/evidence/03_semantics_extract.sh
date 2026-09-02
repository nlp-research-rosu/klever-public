#!/usr/bin/env bash
set -euo pipefail

echo '$ nl -ba /reference/k-proof/verification.k'
nl -ba /reference/k-proof/verification.k
echo '$ nl -ba /reference/k-proof/spec.k'
nl -ba /reference/k-proof/spec.k
echo '$ nl -ba /reference/k-proof/solution.py'
nl -ba /reference/k-proof/solution.py
echo '$ nl -ba /reference/k-proof/solution.mpy'
nl -ba /reference/k-proof/solution.mpy
echo '$ sed -n relevant controls.k rules'
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k | sed -n '8,31p;50,75p'
echo '$ sed -n relevant str.k rules'
nl -ba /reference/k-proof/reference-semantics/semantics/str.k | sed -n '7,41p'
echo '$ sed -n relevant operators.k rules'
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k | sed -n '10,20p'
echo '$ rg simplification /reference/k-proof/verification.k'
if ! rg -n 'simplification' /reference/k-proof/verification.k; then
  echo 'NO simplification attributes'
fi
