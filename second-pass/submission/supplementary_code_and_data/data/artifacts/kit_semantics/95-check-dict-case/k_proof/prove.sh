#!/usr/bin/env bash
set -eu

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

proof_run_dir=$(mktemp -d)
krun smoke.mpy --definition runtime-kompiled \
  | tee "$proof_run_dir/fixed.out"

python3 test_solution.py

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

krun smoke.mpy --definition verification-kompiled \
  | tee "$proof_run_dir/extended.out"
diff -u "$proof_run_dir/fixed.out" "$proof_run_dir/extended.out"

kompile --backend haskell connection.k \
  --main-module CONNECTION \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled

kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop,SPEC.target \
  --trusted SPEC.loop

if kprove spec-vacuity.k \
     --definition verification-kompiled \
     --spec-module SPEC-VACUITY; then
  echo "ERROR: false-postcondition mutation unexpectedly proved"
  exit 1
else
  echo "EXPECTED FAILURE: empty dictionary actually returned false"
fi
