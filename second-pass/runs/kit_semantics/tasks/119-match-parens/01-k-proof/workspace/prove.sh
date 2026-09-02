#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py
python3 check-spec-body.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

python3 py2mpy.py krun-tests.py > krun-tests.mpy
python3 - <<'PY'
import ast
from pathlib import Path

solution = ast.parse(Path('solution.py').read_text()).body[0]
harness = ast.parse(Path('krun-tests.py').read_text()).body[0]
assert ast.dump(solution, include_attributes=False) == ast.dump(
    harness, include_attributes=False
)
print('harness-body-identity: PASS')
PY
krun krun-tests.mpy --definition runtime-kompiled --output json \
  | python3 check-krun-json.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-first
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-second
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

python3 differential-test.py

sed \
  -e 's/^module SPEC$/module SPEC-VACUITY/' \
  -e 's/ensures ?RESULT ==K matchAnswer(A, B)/ensures ?RESULT ==K str(iCons(88, .IntSeq))/' \
  spec.k > spec-vacuity.k
sed \
  -e 's/^module SPEC$/module SPEC-BODY-MUTATION/' \
  -e 's/Return(Str("No"))/Return(Str("Yes"))/' \
  spec.k > spec-body-mutation.k

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY 2>&1 | tee vacuity.log
vacuity_status=${PIPESTATUS[0]}
set -e
if [[ ${vacuity_status} -eq 0 ]]; then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' vacuity.log
echo "vacuity mutation: EXPECTED FAILURE (exit ${vacuity_status})"

set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION 2>&1 | tee body-mutation.log
body_status=${PIPESTATUS[0]}
set -e
if [[ ${body_status} -eq 0 ]]; then
  echo "ERROR: body mutation unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' body-mutation.log
echo "body mutation: EXPECTED FAILURE (exit ${body_status})"
