#!/usr/bin/env bash
set -euo pipefail

nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/solution.mpy
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/reference-semantics/semantics/syntax.k \
  | sed -n '9,61p'
nl -ba /reference/k-proof/reference-semantics/semantics/core.k \
  | sed -n '25,60p;123,210p'
nl -ba /reference/k-proof/reference-semantics/semantics/call.k \
  | sed -n '1,90p'
nl -ba /reference/k-proof/reference-semantics/semantics/functions.k \
  | sed -n '60,105p'
nl -ba /reference/k-proof/reference-semantics/semantics/controls.k \
  | sed -n '47,60p'
nl -ba /reference/k-proof/reference-semantics/semantics/operators.k \
  | sed -n '1,22p'
nl -ba /reference/k-proof/reference-semantics/semantics/int.k \
  | sed -n '1,32p'
