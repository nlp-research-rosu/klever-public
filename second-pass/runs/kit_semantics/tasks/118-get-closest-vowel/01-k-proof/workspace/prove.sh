#!/usr/bin/env bash
set -euo pipefail
set -x

python3 py2mpy.py solution.py > solution.mpy

kompile \
  --backend llvm \
  reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
krun concrete-tests.mpy --definition runtime-kompiled
python3 validate.py

kompile \
  --backend haskell \
  foundation.k \
  --main-module FOUNDATION \
  --syntax-module FOUNDATION-SYNTAX \
  --output-definition connection-kompiled
kprove \
  connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

kompile \
  --backend haskell \
  helper-verification.k \
  --main-module HELPER-VERIFICATION \
  --syntax-module HELPER-VERIFICATION-SYNTAX \
  --output-definition loop-connection-kompiled
kprove \
  loop-connection-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-CONNECTION-SPEC

kompile \
  --backend haskell \
  verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled

kast \
  --definition verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module \
  --expression getClosestProgram \
  --expand-macros \
  --output kore \
  > /tmp/get-closest-proof-program.kore
kast \
  --definition verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module \
  solution.mpy \
  --expand-macros \
  --output kore \
  > /tmp/get-closest-solution-program.kore
cmp \
  /tmp/get-closest-proof-program.kore \
  /tmp/get-closest-solution-program.kore
wc -c \
  /tmp/get-closest-proof-program.kore \
  /tmp/get-closest-solution-program.kore

kprove \
  spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

expect_kprove_failure() {
  if "$@"; then
    echo "ERROR: negative validation probe unexpectedly proved" >&2
    return 1
  else
    local exit_code=$?
    echo "Expected non-zero validation-probe exit: ${exit_code}"
  fi
}

expect_kprove_failure \
  kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
expect_kprove_failure \
  kprove helper-body-mutation-spec.k \
  --definition connection-kompiled \
  --spec-module HELPER-BODY-MUTATION-SPEC
expect_kprove_failure \
  kprove loop-body-mutation-spec.k \
  --definition verification-kompiled \
  --spec-module LOOP-BODY-MUTATION-SPEC
expect_kprove_failure \
  kprove continuation-mutation-spec.k \
  --definition verification-kompiled \
  --spec-module CONTINUATION-MUTATION-SPEC
