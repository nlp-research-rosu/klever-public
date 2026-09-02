#!/usr/bin/env bash
set -euo pipefail
set -x

nl -ba /reference/k-proof/verification.k
nl -ba /reference/k-proof/spec.k
nl -ba /reference/k-proof/solution.py
nl -ba /reference/k-proof/reference-semantics/semantics/int.k
nl -ba /reference/k-proof/reference-semantics/semantics/bool.k
nl -ba /reference/k-proof/reference-semantics/semantics/str.k
sed -n '1,165p' /reference/k-proof/reference-semantics/semantics/float.k | nl -ba
sed -n '1,40p' /reference/k-proof/reference-semantics/semantics/operators.k | nl -ba
nl -ba /reference/klean-generation/generated/Klean105ByLength/Lemmas.lean
nl -ba /candidate/Proof.lean
