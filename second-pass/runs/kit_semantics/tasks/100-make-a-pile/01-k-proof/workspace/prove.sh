#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 -m py_compile solution.py validate.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun smoke.mpy --definition runtime-kompiled \
  2> smoke.err | tee smoke.out

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  2> proof.err | tee proof.out

python3 validate.py | tee validation.out

set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity.out 2> vacuity.err
vacuity_status=$?

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  > body-mutation.out 2> body-mutation.err
body_mutation_status=$?
set -e

if [ "$vacuity_status" -eq 0 ]; then
  echo "ERROR: false returned-reference mutation unexpectedly proved" >&2
  exit 1
fi

if [ "$body_mutation_status" -eq 0 ]; then
  echo "ERROR: changed implementation body unexpectedly proved" >&2
  exit 1
fi

printf 'EXPECTED FAILURE: spec-vacuity.k exited %s\n' "$vacuity_status"
printf 'EXPECTED FAILURE: spec-body-mutation.k exited %s\n' \
  "$body_mutation_status"
