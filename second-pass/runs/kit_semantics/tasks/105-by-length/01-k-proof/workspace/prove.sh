#!/usr/bin/env bash
set -euo pipefail

mkdir -p proof-logs

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
head -n 21 concrete_tests.py | cmp solution.py -

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled \
  2>&1 | tee proof-logs/kompile-llvm.log

krun concrete_tests.mpy \
  --definition runtime-kompiled \
  --output-file concrete-krun.out
tr -d '[:space:]' < concrete-krun.out \
  | rg -q '<k>.K</k>.*<exc>NoExc</exc>.*<exit-code>0</exit-code>'
rg -n -A2 '<exc>|<exit-code>' concrete-krun.out \
  | tee proof-logs/krun-summary.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  2>&1 | tee proof-logs/kompile-haskell.log

kast solution.mpy \
  --definition verification-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file solution-parsed.kore
kast --expression solutionModule \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore \
  --output-file claimed-solution.kore
cmp solution-parsed.kore claimed-solution.kore

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.collect-loop \
  2>&1 | tee proof-logs/kprove-loop.log

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2>&1 | tee proof-logs/kprove-all.log

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > proof-logs/kprove-vacuity.log 2>&1
vacuity_status=$?
set -e
test "${vacuity_status}" -ne 0
rg -m1 'WarnStuckClaimState' proof-logs/kprove-vacuity.log

set +e
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > proof-logs/kprove-body-mutation.log 2>&1
body_mutation_status=$?
set -e
test "${body_mutation_status}" -ne 0
rg -m1 'WarnStuckClaimState' proof-logs/kprove-body-mutation.log

python3 differential_tests.py \
  2>&1 | tee proof-logs/differential.log
