#!/usr/bin/env bash
set -euo pipefail
set -x

python3 /reference/py2mpy.py solution.py > solution.mpy
python3 generate_proof_artifacts.py

sha256sum \
  /tmp/audit-work/candidate-src/solution-program.k \
  solution-program.k

if cmp /tmp/audit-work/candidate-src/solution-program.k solution-program.k
then
  echo "ERROR: material source mutation did not change executed K program term"
  exit 1
else
  echo "executed solutionProgram term changed as expected"
fi

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition body-mutation-kompiled

set +e
kprove spec.k \
  --definition body-mutation-kompiled \
  --spec-module BF-SPEC
mutation_rc=$?
set -e

echo "body mutation kprove exit=$mutation_rc"
if test "$mutation_rc" -eq 0
then
  echo "ERROR: proof survived a false material body mutation"
  exit 1
fi
echo "body sensitivity: material executed-body mutation rejected as expected"
