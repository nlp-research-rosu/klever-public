#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

proof_build="$(mktemp -d "$PWD/.proof-build.XXXXXX")"
echo "proof build: $proof_build"

# Recreate the required transliteration and make sure it is the exact program
# whose syntax is embedded in the implementation-specific K claims.
python3 py2mpy.py solution.py > solution.mpy
test "$(sha256sum solution.mpy | cut -d' ' -f1)" = \
  "b7281d4d4cfc59b4bbfc0642162bd813928025a7a4858c8abea1730fda9486d4"

# Exercise every example from prompt.py with the concrete LLVM semantics.
cp solution.py "$proof_build/concrete_tests.py"
sed -n '/^assert /,$p' concrete_assertions.py >> "$proof_build/concrete_tests.py"
python3 py2mpy.py "$proof_build/concrete_tests.py" \
  > "$proof_build/concrete_tests.mpy"
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof_build/runtime-kompiled"
krun "$proof_build/concrete_tests.mpy" \
  --definition "$proof_build/runtime-kompiled" \
  --output pretty | tee "$proof_build/krun.out"
grep -A 1 '<exc>' "$proof_build/krun.out" | grep -q 'NoExc'
grep -A 1 '<exit-code' "$proof_build/krun.out" | grep -q '0'

# Prove the divisor-loop lemma without either loop summary available.
kompile verification.k \
  --backend haskell \
  --main-module COUNT-UP-TO-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof_build/inner-proof-kompiled"
kprove spec.k \
  --definition "$proof_build/inner-proof-kompiled" \
  --spec-module COUNT-UP-TO-INNER-LOOP-SPEC

# Prove the candidate-loop lemma using only the proved divisor-loop lemma.
kompile verification.k \
  --backend haskell \
  --main-module COUNT-UP-TO-WITH-INNER \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof_build/outer-proof-kompiled"
kprove spec.k \
  --definition "$proof_build/outer-proof-kompiled" \
  --spec-module COUNT-UP-TO-OUTER-LOOP-SPEC

# Prove the entry body for N >= 2 and the non-negative boundary 0 <= N < 2
# using the two independently proved loop lemmas.
kompile verification.k \
  --backend haskell \
  --main-module COUNT-UP-TO-WITH-OUTER \
  --syntax-module MPY-SYNTAX \
  --output-definition "$proof_build/entry-proof-kompiled"
kprove spec.k \
  --definition "$proof_build/entry-proof-kompiled" \
  --spec-module COUNT-UP-TO-ENTRY-SPEC
kprove spec.k \
  --definition "$proof_build/entry-proof-kompiled" \
  --spec-module COUNT-UP-TO-BOUNDARY-SPEC
