#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Translate the submitted implementation with the fixed front end.
python3 -m py_compile solution.py
python3 py2mpy.py solution.py > solution.mpy

# The concrete test driver begins with the exact submitted implementation.
diff -u solution.py <(sed -n '1,7p' concrete-tests.py)
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Concrete execution under the required LLVM definition.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty

# Symbolic definition and three modular positive proofs.  Each established
# lemma is trusted only in a later command, after its own command proved #Top.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.member-fold \
  --output pretty
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.member-fold,SPEC.common-loop \
  --trusted SPEC.member-fold \
  --output pretty
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.member-fold,SPEC.common-loop,SPEC.common-function \
  --trusted SPEC.member-fold,SPEC.common-loop \
  --output pretty
