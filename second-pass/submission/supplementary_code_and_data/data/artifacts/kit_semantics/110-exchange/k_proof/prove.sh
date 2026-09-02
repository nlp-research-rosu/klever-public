#!/usr/bin/env bash
set -euo pipefail

expect_failure() {
  set +e
  "$@"
  status=$?
  set -e
  if [ "$status" -eq 0 ]; then
    echo "UNEXPECTED SUCCESS: $*" >&2
    return 1
  fi
  echo "EXPECTED FAILURE (exit $status): $*"
}

# Required translation and concrete execution under the frozen reference
# semantics, using its required LLVM modules.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled > krun-reference.out

# Bridge-free connection definition and the connected target definition.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Positive proofs.  Each command must print #Top and exit 0.
kprove connection-spec.k \
  --definition verification-base-kompiled \
  --spec-module CONNECTION-SPEC
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Independent and concrete evidence for the modeled numeric domain.
python3 differential.py
python3 py2mpy.py k-numeric-tests.py > k-numeric-tests.mpy
kompile verification.k \
  --backend llvm \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-runtime-kompiled
krun k-numeric-tests.mpy \
  --definition verification-runtime-kompiled \
  > krun-numeric-extended.out

# Negative validation probes must fail.
expect_failure kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
expect_failure kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
expect_failure kprove connection-wrong-spec.k \
  --definition verification-base-kompiled \
  --spec-module CONNECTION-WRONG-SPEC
expect_failure kprove connection-wrong-odd-spec.k \
  --definition verification-base-kompiled \
  --spec-module CONNECTION-WRONG-ODD-SPEC
