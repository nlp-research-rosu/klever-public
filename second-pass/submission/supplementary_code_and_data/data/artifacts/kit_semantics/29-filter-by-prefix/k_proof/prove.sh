#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-tests.py > concrete-tests.mpy
python3 differential_test.py

kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-tests.mpy \
  --definition runtime-kompiled \
  --output pretty \
  --output-file concrete-tests.out
python3 - <<'PY'
import re

text = open("concrete-tests.out", encoding="utf-8").read()
assert re.search(r"<k>\s*\.K\s*</k>", text)
assert re.search(r"<exc>\s*NoExc\s*</exc>", text)
assert re.search(r"<exit-code>\s*0\s*</exit-code>", text)
print("LLVM concrete assertions: PASS")
PY

# Bridge-free proof of iterator value/control equivalence.
kompile --backend haskell domain.k \
  --main-module STRING-SEQUENCE-DOMAIN \
  --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k \
  --definition connection-kompiled \
  --spec-module CONNECTION-SPEC

# Bridge-free proof of the exact loop, return, and frame-cleanup summary.
kompile --backend haskell verification-core.k \
  --main-module VERIFICATION-CORE \
  --syntax-module MPY-SYNTAX \
  --output-definition loop-connection-kompiled
kprove loop-connection-spec.k \
  --definition loop-connection-kompiled \
  --spec-module LOOP-CONNECTION-SPEC

# Final target definition and both required claims.
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kast solution.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --output kore > program-source.kore
kast \
  --expression 'filterByPrefixProgram' \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Module \
  --expand-macros \
  --output kore > program-macro.kore
cmp program-source.kore program-macro.kore
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Fixed-versus-extended witnesses for distinct iterator and loop outcomes.
kprove bridge-witness-fixed.k \
  --definition loop-connection-kompiled \
  --spec-module BRIDGE-WITNESS-FIXED
kprove bridge-witness-extended.k \
  --definition verification-kompiled \
  --spec-module BRIDGE-WITNESS-EXTENDED

# The body mutant needs its syntax macros in a separately compiled definition.
kompile --backend haskell body-mutant.k \
  --main-module BODY-MUTANT \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mutant-kompiled

if kprove bridge-witness-negative.k \
  --definition verification-kompiled \
  --spec-module BRIDGE-WITNESS-NEGATIVE \
  --claims BRIDGE-WITNESS-NEGATIVE.wrong-iterator-value \
  > negative-iterator.out 2>&1
then
  echo "wrong iterator value unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' negative-iterator.out
echo "wrong iterator value: EXPECTED FAILURE"

if kprove bridge-witness-negative.k \
  --definition verification-kompiled \
  --spec-module BRIDGE-WITNESS-NEGATIVE \
  --claims BRIDGE-WITNESS-NEGATIVE.wrong-loop-value \
  > negative-loop.out 2>&1
then
  echo "wrong loop value unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' negative-loop.out
echo "wrong loop value: EXPECTED FAILURE"

if kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity.out 2>&1
then
  echo "false postcondition unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' vacuity.out
echo "false postcondition: EXPECTED FAILURE"

if kprove spec-body-mutant.k \
  --definition body-mutant-kompiled \
  --spec-module SPEC-BODY-MUTANT \
  > body-mutant.out 2>&1
then
  echo "mutated body unexpectedly proved" >&2
  exit 1
fi
rg -q 'WarnStuckClaimState' body-mutant.out
echo "mutated body: EXPECTED FAILURE"

echo "all proof and validation checks passed"
