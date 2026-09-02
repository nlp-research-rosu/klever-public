#!/usr/bin/env bash
set -euo pipefail

# Keep every run collision-free and preserve its compiled definitions for audit.
PROOF_BUILD=$(mktemp -d -p "$PWD" .kproof.XXXXXX)

# Required translation and concrete LLVM execution.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$PROOF_BUILD/runtime-kompiled"
krun smoke.mpy \
  --definition "$PROOF_BUILD/runtime-kompiled" \
  --output none

# Proof rung 1: the helper's structural loop cases.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition "$PROOF_BUILD/base-kompiled"
kprove spec.k \
  --definition "$PROOF_BUILD/base-kompiled" \
  --spec-module SPEC-INNER

# Proof rung 2: the complete helper call, using only rung 1's proved summary.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-WITH-INNER \
  --syntax-module MPY-SYNTAX \
  --output-definition "$PROOF_BUILD/inner-kompiled"
kprove spec.k \
  --definition "$PROOF_BUILD/inner-kompiled" \
  --spec-module SPEC-HELPER

# Proof rung 3: the outer all-pairs traversal.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-WITH-HELPER \
  --syntax-module MPY-SYNTAX \
  --output-definition "$PROOF_BUILD/helper-kompiled"
kprove spec.k \
  --definition "$PROOF_BUILD/helper-kompiled" \
  --spec-module SPEC-OUTER

# Proof rung 4: the required public entry point.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-WITH-OUTER \
  --syntax-module MPY-SYNTAX \
  --output-definition "$PROOF_BUILD/outer-kompiled"
kprove spec.k \
  --definition "$PROOF_BUILD/outer-kompiled" \
  --spec-module SPEC-ENTRY

# Proof rung 5: load the exact solution.mpy tree and call the entry point.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-WITH-ENTRY \
  --syntax-module MPY-SYNTAX \
  --output-definition "$PROOF_BUILD/entry-kompiled"
kprove spec.k \
  --definition "$PROOF_BUILD/entry-kompiled" \
  --spec-module SPEC

echo "Proof artifacts: $PROOF_BUILD"
