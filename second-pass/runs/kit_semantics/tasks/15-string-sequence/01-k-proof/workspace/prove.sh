#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Reproduce the translator outputs and check that the smoke artifact embeds the
# exact solution source before adding its top-level assertions.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
solution_line_count=$(wc -l < solution.py)
head -n "$solution_line_count" smoke.py | cmp - solution.py

# Concrete execution under the required LLVM definition.
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled | tee smoke.krun.out
rg -Uq '<exit-code>[[:space:]]*0[[:space:]]*</exit-code>' smoke.krun.out

# Symbolic proof: this all-claims command loads the loop invariant alongside
# the entry claim and must print #Top with exit status 0.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC | tee proof.out
rg -qx '#Top' proof.out

# Gate A negative probes.  Both are expected to be rejected.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY > vacuity.out 2>&1
vacuity_status=$?
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION > body-mutation.out 2>&1
body_mutation_status=$?
set -e

if (( vacuity_status == 0 )); then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
fi
if (( body_mutation_status == 0 )); then
  echo "ERROR: comma-separator body mutation unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' vacuity.out
rg -Fq 'str ( iCons ( 48 , .IntSeq ) )' vacuity.out
rg -q 'WarnStuckClaimState' body-mutation.out
rg -Fq 'iCons ( 44 ,' body-mutation.out

# Independent CPython differential evidence.
python3 differential_test.py | tee differential.out

printf 'expected-failure vacuity exit: %s\n' "$vacuity_status"
printf 'expected-failure body mutation exit: %s\n' "$body_mutation_status"
