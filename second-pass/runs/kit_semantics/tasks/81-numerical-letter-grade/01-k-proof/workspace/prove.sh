#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 check_artifacts.py | tee artifact-check.out
python3 differential.py | tee differential.out

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  2>&1 | tee llvm-compile.out

krun smoke.mpy --definition runtime-kompiled | tee concrete.out
python3 - <<'PY'
from pathlib import Path

result = Path("concrete.out").read_text(encoding="utf-8")
if "<k>\n    .K\n  </k>" not in result:
    raise SystemExit("concrete execution did not finish with .K")
if "<exc>\n    NoExc\n  </exc>" not in result:
    raise SystemExit("concrete execution raised an exception")
if "<exit-code>\n    0\n  </exit-code>" not in result:
    raise SystemExit("concrete execution did not report exit code 0")
print("LLVM smoke checks: PASS")
PY

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  2>&1 | tee haskell-compile.out

# Confirm that the proof macro expands to the exact translated solution term.
kast --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  solution.mpy > solution-term.kore
kast --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --expression 'GRADE-PROGRAM' > proof-term.kore
cmp solution-term.kore proof-term.kore
echo "KAST macro identity: PASS"

# Required positive target proof: both the loop invariant and entry claim.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee target-proof.out
grep -qx '#Top' target-proof.out

# A5: a false postcondition for the realizable empty input must be rejected.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity.out 2>&1
vacuity_status=$?
set -e
if [[ "$vacuity_status" -eq 0 ]]; then
  echo "ERROR: false-postcondition probe unexpectedly proved" >&2
  exit 1
fi
grep -q 'WarnStuckClaimState' vacuity.out
echo "false-postcondition probe: EXPECTED FAILURE (exit $vacuity_status)"

# A1: a materially wrong real loop body must invalidate the invariant.
kompile mutation.k \
  --backend haskell \
  --main-module MUTATION \
  --syntax-module MPY-SYNTAX \
  --output-definition mutation-kompiled \
  2>&1 | tee mutation-compile.out

set +e
kprove spec-body-mutation.k \
  --definition mutation-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > body-mutation.out 2>&1
body_mutation_status=$?
set -e
if [[ "$body_mutation_status" -eq 0 ]]; then
  echo "ERROR: body-mutation probe unexpectedly proved" >&2
  exit 1
fi
grep -q 'WarnStuckClaimState' body-mutation.out
grep -q 'iCons ( 90 , .IntSeq )' body-mutation.out
echo "body-sensitivity probe: EXPECTED FAILURE (exit $body_mutation_status)"
