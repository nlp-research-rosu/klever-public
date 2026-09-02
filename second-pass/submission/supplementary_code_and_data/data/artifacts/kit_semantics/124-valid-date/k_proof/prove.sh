#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

krun concrete-tests.mpy --definition runtime-kompiled
python3 test_solution.py

# Check that the proof's named program constant is exactly solution.mpy after
# both are parsed to KORE (explicit .Stmts is only needed inside K source).
sed -n '13,166p' verification.k \
  | sed -e '1s/^[[:space:]]*=> //' -e 's/\.Stmts//g' \
  > verification-program.mpy
kast solution.mpy \
  --definition runtime-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --output kore \
  --output-file /tmp/solution.kore
kast verification-program.mpy \
  --definition runtime-kompiled \
  --module MPY-SYNTAX \
  --sort Module \
  --output kore \
  --output-file /tmp/verification-program.kore
cmp /tmp/solution.kore /tmp/verification-program.kore

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.valid-date-10
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.valid-date-non10

# Gate A5: a valid witness must not prove the deliberately false result.
if kprove spec-vacuity.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY; then
  echo "ERROR: false-result mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: false-result mutation was rejected"
fi

# Gate A1: changing February's bound in the executed body from 29 to 28 must
# break the universal connection to the unchanged calendar summary.
sed '137s/Int(29)/Int(28)/' verification.k > verification-mutant.k
sed -e '1s/verification.k/verification-mutant.k/' \
    -e 's/^module SPEC$/module SPEC-MUTANT/' \
    spec.k > spec-mutant.k
kompile verification-mutant.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-mutant-kompiled
if kprove spec-mutant.k \
    --definition verification-mutant-kompiled \
    --spec-module SPEC-MUTANT \
    --claims SPEC-MUTANT.valid-date-10; then
  echo "ERROR: body mutation unexpectedly proved" >&2
  exit 1
else
  echo "EXPECTED FAILURE: body mutation was rejected"
fi
