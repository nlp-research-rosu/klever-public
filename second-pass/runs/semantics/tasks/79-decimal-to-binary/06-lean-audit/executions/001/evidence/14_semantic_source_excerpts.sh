#!/usr/bin/env bash
set -euo pipefail

echo '$ nl -ba /reference/k-proof/solution.py'
nl -ba /reference/k-proof/solution.py

echo '$ nl -ba /reference/k-proof/solution.mpy'
nl -ba /reference/k-proof/solution.mpy

echo '$ nl -ba /reference/k-proof/spec.k'
nl -ba /reference/k-proof/spec.k

echo '$ nl -ba /reference/k-proof/prove.sh'
nl -ba /reference/k-proof/prove.sh

echo '$ nl -ba /reference/k-proof/reference-semantics/semantics/subscript.k | sed -n 50,140p'
nl -ba /reference/k-proof/reference-semantics/semantics/subscript.k | sed -n '50,140p'

echo '$ nl -ba /reference/k-proof/reference-semantics/semantics/builtins.k | sed -n 103,125p'
nl -ba /reference/k-proof/reference-semantics/semantics/builtins.k | sed -n '103,125p'

echo '$ nl -ba /candidate/Proof.lean | sed -n 1,190p'
nl -ba /candidate/Proof.lean | sed -n '1,190p'
