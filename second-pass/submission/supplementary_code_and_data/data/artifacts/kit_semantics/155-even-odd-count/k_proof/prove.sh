#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and all concrete/mutation harnesses.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 py2mpy.py body_mutant.py > body_mutant.mpy
python3 make_program_spec.py identity solution.mpy > identity-spec.k
python3 make_program_spec.py mutant body_mutant.mpy > body-mutation-spec.k

# Ensure the concrete harness contains exactly the submitted function AST.
python3 - <<'PY'
import ast
from pathlib import Path

solution = ast.parse(Path("solution.py").read_text()).body[0]
harness = ast.parse(Path("concrete_tests.py").read_text()).body[0]
assert ast.dump(solution, include_attributes=False) == ast.dump(
    harness, include_attributes=False
)
print("Harness function AST matches solution.py")
PY

# Required LLVM execution of the supplied reference semantics.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  2>&1 | tee llvm-build.log
krun concrete_tests.mpy --definition runtime-kompiled \
  2>&1 | tee concrete-krun.log
rg -q "NoExc" concrete-krun.log

# Bridge-free definition: prove the exact loop connection theorem and the
# generated solution.mpy-to-evenOddClosure identity theorem.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-verification-kompiled \
  2>&1 | tee loop-build.log
kprove spec.k \
  --definition loop-verification-kompiled \
  --spec-module LOOP-PROOF \
  2>&1 | tee loop-proof.log
rg -q "^#Top$" loop-proof.log
kprove identity-spec.k \
  --definition loop-verification-kompiled \
  --spec-module IDENTITY-SPEC \
  2>&1 | tee identity-proof.log
rg -q "^#Top$" identity-proof.log

# Extended definition: use only the exact-context bridge justified above.
kompile --backend haskell verification-with-lemma.k \
  --main-module VERIFICATION-WITH-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  2>&1 | tee verification-build.log
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee target-proof.log
rg -q "^#Top$" target-proof.log
kprove context-spec.k \
  --definition verification-kompiled \
  --spec-module CONTEXT-SPEC \
  2>&1 | tee context-proof.log
rg -q "^#Top$" context-proof.log

# A5 false-postcondition probe and A1 body-sensitivity mutation.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity.log 2>&1
vacuity_status=$?
kprove body-mutation-spec.k \
  --definition verification-kompiled \
  --spec-module BODY-MUTATION-SPEC \
  > body-mutation.log 2>&1
body_mutation_status=$?
set -e

if [[ "$vacuity_status" -eq 0 ]]; then
  echo "ERROR: false postcondition unexpectedly proved" >&2
  exit 1
fi
if [[ "$body_mutation_status" -eq 0 ]]; then
  echo "ERROR: mutated body unexpectedly proved" >&2
  exit 1
fi
rg -q "WarnStuckClaimState" vacuity.log
rg -Fq "decEven ( N ) +Int 1" vacuity.log
rg -q "WarnStuckClaimState" body-mutation.log
rg -Fq "tuple ( vCons ( 0 , vCons ( 0" body-mutation.log
printf 'Expected failures: vacuity=%s body-mutation=%s\n' \
  "$vacuity_status" "$body_mutation_status"

# Independent CPython oracle over a broad finite sample.
python3 differential_test.py | tee differential.log
