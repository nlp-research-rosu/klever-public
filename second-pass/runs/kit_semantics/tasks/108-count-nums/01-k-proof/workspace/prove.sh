#!/usr/bin/env bash
set -euo pipefail

# Translate the preserved source and the concrete assertion harness.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy

# Concrete and independent executable checks.
python3 concrete-tests.py
python3 differential_test.py

# Concrete execution uses the supplied semantics without proof extensions.
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled \
  2> concrete-krun.err | tee concrete-krun.out

# Symbolic proof definition: import the supplied MPY semantics read-only.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Together these two positive commands prove all seven claims in spec.k.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.digit-loop,SPEC.outer-loop-empty,SPEC.outer-loop-step,SPEC.call-setup-nonempty,SPEC.outer-loop-initial,SPEC.count-nums-nonempty \
  2>&1 | tee kprove-entry-nonempty.log
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.count-nums-empty \
  2>&1 | tee kprove-entry-empty.log

# Gate A validation definition and expected-failure probes.
kompile --backend haskell validation.k \
  --main-module VALIDATION \
  --syntax-module MPY-SYNTAX \
  --output-definition validation-kompiled

set +e
kprove spec-vacuity.k \
  --definition validation-kompiled \
  --spec-module SPEC-VACUITY \
  2>&1 | tee kprove-vacuity.log
vacuity_status=${PIPESTATUS[0]}
set -e
echo "EXPECTED_NONZERO_STATUS=$vacuity_status"
if (( vacuity_status == 0 )); then
  echo "The false-postcondition probe unexpectedly proved." >&2
  exit 1
fi

set +e
kprove spec-body-mutation.k \
  --definition validation-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  2>&1 | tee kprove-body-mutation.log
mutation_status=${PIPESTATUS[0]}
set -e
echo "EXPECTED_NONZERO_STATUS=$mutation_status"
if (( mutation_status == 0 )); then
  echo "The body-mutation probe unexpectedly proved." >&2
  exit 1
fi
