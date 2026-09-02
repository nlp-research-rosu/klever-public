#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.nix-profile/bin:$PATH"

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  2>&1 | tee llvm-build.out

krun smoke.mpy --definition runtime-kompiled \
  2>&1 | tee krun-smoke.out

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  2>&1 | tee haskell-build.out

# This is the required positive target-proof command.  Keeping all claims in
# the command makes the two loop circularities available to the entry claim.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee kprove-positive.out
rg -q '^#Top$' kprove-positive.out

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  2>&1 | tee vacuity.out
vacuity_status=${PIPESTATUS[0]}

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  2>&1 | tee body-mutation.out
body_mutation_status=${PIPESTATUS[0]}
set -e

if [[ $vacuity_status -eq 0 ]]; then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' vacuity.out
echo "EXPECTED FAILURE: false-result mutation exited $vacuity_status"

if [[ $body_mutation_status -eq 0 ]]; then
  echo "ERROR: body mutation unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' body-mutation.out
echo "EXPECTED FAILURE: body mutation exited $body_mutation_status"

python3 test_solution.py 2>&1 | tee differential.out
