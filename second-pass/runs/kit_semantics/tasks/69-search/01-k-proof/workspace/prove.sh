#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 check_program_identity.py
python3 differential_test.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  2>&1 | tee llvm-kompile.log

krun concrete_tests.mpy --definition runtime-kompiled \
  2>&1 | tee krun.log
rg -U -q '<k>[[:space:]]*\.K[[:space:]]*</k>' krun.log
rg -U -q '<exc>[[:space:]]*NoExc[[:space:]]*</exc>' krun.log
rg -U -q '<exit-code>[[:space:]]*0[[:space:]]*</exit-code>' krun.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  2>&1 | tee haskell-kompile.log

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee kprove.log
rg -x -q '#Top' kprove.log

sed \
  -e 's/module SPEC$/module SPEC-VACUITY/' \
  -e 's/=> searchSummary(INPUT, INPUT, -1) ~> .K/=> searchSummary(INPUT, INPUT, -1) +Int 1 ~> .K/' \
  spec.k > spec-vacuity.k

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity.log 2>&1
then
  echo "ERROR: false-postcondition mutation unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' vacuity.log
if rg -x -q '#Top' vacuity.log; then
  echo "ERROR: false-postcondition mutation printed #Top" >&2
  exit 1
fi
echo "false-postcondition mutation: EXPECTED FAILURE"

sed \
  -e 's/module SPEC$/module SPEC-BODY-MUTATION/' \
  -e '0,/Assign(Name("answer"), UnaryOp("-", Int(1)))/s//Assign(Name("answer"), UnaryOp("-", Int(2)))/' \
  spec.k > spec-body-mutation.k

if kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > body-mutation.log 2>&1
then
  echo "ERROR: body mutation unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' body-mutation.log
if rg -x -q '#Top' body-mutation.log; then
  echo "ERROR: body mutation printed #Top" >&2
  exit 1
fi
echo "body-sensitivity mutation: EXPECTED FAILURE"
