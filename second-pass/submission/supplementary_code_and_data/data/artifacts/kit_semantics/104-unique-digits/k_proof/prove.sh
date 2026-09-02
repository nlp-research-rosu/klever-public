#!/usr/bin/env bash
set -euo pipefail

# Translation identity and executable evidence.
python3 py2mpy.py solution.py > solution.mpy
cmp <(python3 py2mpy.py solution.py) solution.mpy
python3 validate.py
python3 py2mpy.py concrete.py > concrete.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete.mpy --definition runtime-kompiled | tee concrete.krun
python3 validate_krun.py

# Positive symbolic proof.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Gate A body-sensitivity and result non-vacuity probes.
sed -e 's/module SPEC/module SPEC-BODY-MUTATION/' \
    -e 's/Int(2)/Int(3)/g' \
    spec.k > spec-body-mutation.k

if kprove spec-body-mutation.k \
     --definition verification-kompiled \
     --spec-module SPEC-BODY-MUTATION \
     --claims SPEC-BODY-MUTATION.digit-loop; then
  echo "ERROR: body mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: body mutation rejected"
fi

sed -e 's/module SPEC/module SPEC-VACUITY/' \
    -e 's/=> ref(1)/=> ref(0)/' \
    spec.k > spec-vacuity.k

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY \
     --claims SPEC-VACUITY.digit-loop,SPEC-VACUITY.outer-loop,SPEC-VACUITY.program; then
  echo "ERROR: false result mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: false result mutation rejected"
fi
