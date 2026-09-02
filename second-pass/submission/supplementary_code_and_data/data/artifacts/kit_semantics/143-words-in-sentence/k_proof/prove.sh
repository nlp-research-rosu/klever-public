#!/usr/bin/env bash
set -euo pipefail

# Recreate the submitted transliteration.
python3 py2mpy.py solution.py > solution.mpy

# Concrete LLVM execution of the prompt examples and boundary cases.
python3 py2mpy.py concrete_examples.py > concrete_examples.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_examples.mpy \
  --definition runtime-kompiled \
  2>&1 | tee concrete_examples.krun.out

# The proof's compile-time program alias must be exactly solution.mpy.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kast solution.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore > solution.ast.kore
kast \
  --expression '#solutionModule' \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore > verification-module.ast.kore
cmp solution.ast.kore verification-module.ast.kore
echo 'AST_IDENTITY: PASS'

# First close the loop circularity, then prove the simultaneous claim set
# containing both the loop invariant and the whole-program claim.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.scan-loop \
  2>&1 | tee proof-loop.out
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee proof-full.out

# Independent executable oracle evidence.
python3 test_solution.py

# Gate A5: appending "x" to the required result is deliberately false.
if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY \
     > spec-vacuity.out 2>&1; then
  echo 'ERROR: false-postcondition mutation unexpectedly proved'
  exit 1
else
  vacuity_status=$?
  echo "EXPECTED_VACUITY_FAILURE_EXIT=${vacuity_status}"
  rg -m 1 'WarnStuckClaimState' spec-vacuity.out
fi

# Gate A1: changing the emitted separator from space to "x" must break the
# connection between execution and the original summary.
kompile verification-body-mutant.k \
  --backend haskell \
  --main-module VERIFICATION-BODY-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-body-mutant-kompiled
if kprove spec-body-mutant.k \
     --definition verification-body-mutant-kompiled \
     --spec-module SPEC-BODY-MUTANT \
     > spec-body-mutant.out 2>&1; then
  echo 'ERROR: body mutation unexpectedly proved'
  exit 1
else
  body_mutant_status=$?
  echo "EXPECTED_BODY_MUTATION_FAILURE_EXIT=${body_mutant_status}"
  rg -m 1 'WarnStuckClaimState' spec-body-mutant.out
fi

echo 'ALL_PROOF_AND_VALIDATION_CHECKS_PASSED'
