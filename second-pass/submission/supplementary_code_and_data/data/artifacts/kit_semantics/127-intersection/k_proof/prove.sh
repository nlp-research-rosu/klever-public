#!/usr/bin/env bash
set -euo pipefail

# Generate the exact constructor program and its K source abbreviation.
python3 py2mpy.py solution.py > solution.mpy
python3 make_solution_module.py > solution-module.k

# Required concrete LLVM execution of the supplied, unmodified semantics.
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py smoke.py > smoke.mpy
krun smoke.mpy --definition runtime-kompiled

# Symbolic proof: all claims, no depth bound.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC 2>&1 | tee proof.out

# Ground execution and independent differential evidence.
krun summary-smoke.mpy \
  --definition verification-kompiled \
  --parser ./parse-verification.sh
python3 validate.py

# Gate A5: a false result claim must be rejected.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY > vacuity.out 2>&1
vacuity_status=$?
set -e
if [[ $vacuity_status -eq 0 ]]; then
  echo "ERROR: false-postcondition mutation unexpectedly proved" >&2
  exit 1
fi
echo "expected vacuity-probe failure: exit=$vacuity_status"

# Gate A1: changing the final YES return to NO must invalidate correctness.
python3 make_mutant.py > solution-mutant.py
python3 py2mpy.py solution-mutant.py > solution-mutant.mpy
python3 make_solution_module.py solution-mutant.mpy \
  --constant mutantSolutionModule \
  --prefix MUTANT-SOLUTION-MODULE > mutant-solution-module.k
python3 check_artifacts.py
kompile --backend haskell mutation-verification.k \
  --main-module MUTATION-VERIFICATION \
  --syntax-module MUTATION-VERIFICATION-SYNTAX \
  --output-definition mutation-verification-kompiled
set +e
kprove spec-body-mutation.k \
  --definition mutation-verification-kompiled \
  --spec-module SPEC-BODY-MUTATION > body-mutation.out 2>&1
body_status=$?
set -e
if [[ $body_status -eq 0 ]]; then
  echo "ERROR: body mutation unexpectedly proved" >&2
  exit 1
fi
echo "expected body-mutation failure: exit=$body_status"

sha256sum \
  prompt.py py2mpy.py solution.py solution.mpy solution-module.k \
  verification.k spec.k reference-semantics/semantics.k
