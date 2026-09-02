#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Regenerate both MPY programs from their Python sources.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 -c 'import ast, pathlib; s = ast.parse(pathlib.Path("solution.py").read_text()).body[0]; h = ast.parse(pathlib.Path("concrete_tests.py").read_text()).body[0]; assert ast.dump(s) == ast.dump(h)'

# Concrete LLVM execution of all examples from prompt.py.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output none

# Symbolic definition: verification.k imports MPY from the supplied semantics.
kompile verification.k \
  --backend haskell \
  --main-module SIMPLE-POWER-VERIFICATION \
  --syntax-module SIMPLE-POWER-VERIFICATION \
  --output-definition verification-kompiled

# Gate the hand-readable solutionModule macro against the translator output.
diff -u \
  <(kast solution.mpy --definition verification-kompiled --module SIMPLE-POWER-VERIFICATION --sort Module --expand-macros --output kore) \
  <(kast --expression solutionModule --definition verification-kompiled --module SIMPLE-POWER-VERIFICATION --sort Module --expand-macros --output kore)

# First prove the inductive loop lemma.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SIMPLE-POWER-SPEC \
  --claims SIMPLE-POWER-SPEC.loop-correct \
  --smt-timeout 10000

# Prove the three terminating guard partitions.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SIMPLE-POWER-SPEC \
  --claims SIMPLE-POWER-SPEC.function-one,SIMPLE-POWER-SPEC.function-below-one,SIMPLE-POWER-SPEC.function-degenerate-base \
  --smt-timeout 10000

# Prove the positive-domain entry point, using the loop claim proved above as
# a lemma in this independent kprove invocation.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SIMPLE-POWER-SPEC \
  --claims SIMPLE-POWER-SPEC.loop-correct,SIMPLE-POWER-SPEC.function-positive-domain \
  --trusted SIMPLE-POWER-SPEC.loop-correct \
  --smt-timeout 10000
