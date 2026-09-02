#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' 'COMMAND: nl -ba frozen verification.k, spec.k, solution.py, solution.mpy'
nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
printf '%s\n' 'COMMAND: nl -ba relevant supplied-semantics rules'
nl -ba /reference/k-proof/reference-semantics/semantics/syntax.k \
  | sed -n '1,58p'
nl -ba /reference/k-proof/reference-semantics/semantics/core.k \
  | sed -n '120,205p'
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k \
  | sed -n '1,47p'
nl -ba /reference/k-proof/reference-semantics/semantics/int.k \
  | sed -n '1,28p'
nl -ba /reference/k-proof/reference-semantics/semantics/call.k \
  | sed -n '15,95p'
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k \
  | sed -n '62,91p'
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k \
  | sed -n '46,55p'
