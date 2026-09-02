#!/usr/bin/env bash
set -euo pipefail

# Translator and source-identity checks.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
cmp -n "$(wc -c < solution.py)" solution.py concrete-tests.py

# Independent executable evidence.
python3 concrete-tests.py
python3 differential-test.py

# Required concrete LLVM build and execution.
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy --definition runtime-kompiled \
  2>&1 | tee concrete-run.log
grep -q '    .K' concrete-run.log
grep -q '    NoExc' concrete-run.log

# Symbolic definition and the complete positive target proof.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee proof-run.log
grep -q '^#Top$' proof-run.log

# Gate A5: the deliberately false result for [0, 0, 0] must be rejected.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  2>&1 | tee mutation-run.log
mutation_status=${PIPESTATUS[0]}
set -e
if [[ "$mutation_status" -eq 0 ]]; then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
fi
grep -q 'WarnStuckClaimState' mutation-run.log
grep -q 'true ~> .K' mutation-run.log

# Gate A1: replacing the exact body by "return False" must also be rejected.
set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  2>&1 | tee body-mutation-run.log
body_mutation_status=${PIPESTATUS[0]}
set -e
if [[ "$body_mutation_status" -eq 0 ]]; then
  echo "ERROR: mutated program body unexpectedly proved" >&2
  exit 1
fi
grep -q 'WarnStuckClaimState' body-mutation-run.log
grep -q 'false ~> .K' body-mutation-run.log

echo "POSITIVE_PROOF=#Top"
echo "FALSE_RESULT_MUTATION=REJECTED"
echo "BODY_MUTATION=REJECTED"
