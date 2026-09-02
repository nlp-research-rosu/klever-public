#!/usr/bin/env bash
set -euo pipefail

export PATH="$HOME/.nix-profile/bin:$PATH"

# Reproduce the fixed AST-to-MPY translations.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy

# Independent CPython differential evidence.
python3 test_solution.py

# Gate A concrete baseline: untouched reference semantics, LLVM backend.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

SMOKE_RESULT_FILE="$(mktemp)"
VACUITY_RESULT_FILE="$(mktemp)"
MUTANT_RESULT_FILE="$(mktemp)"
trap 'rm -f "$SMOKE_RESULT_FILE" "$VACUITY_RESULT_FILE" "$MUTANT_RESULT_FILE"' EXIT

krun smoke.mpy --definition runtime-kompiled | tee "$SMOKE_RESULT_FILE"
grep -F '"example" |-> 2' "$SMOKE_RESULT_FILE"
grep -F '"singleton" |-> 0' "$SMOKE_RESULT_FILE"
grep -F '"mixed_sign" |-> 2' "$SMOKE_RESULT_FILE"

# Symbolic definition and the positive, full-domain target proof.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.add-loop

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC

# Gate A5: a false result must not prove.
set +e
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY 2>&1 | tee "$VACUITY_RESULT_FILE"
VACUITY_STATUS="${PIPESTATUS[0]}"
set -e
if [[ "$VACUITY_STATUS" -eq 0 ]]; then
  echo "ERROR: false-postcondition probe unexpectedly proved" >&2
  exit 1
fi
grep -F '"$result" |-> 2' "$VACUITY_RESULT_FILE"
echo "EXPECTED FAILURE: false-postcondition probe exited $VACUITY_STATUS"

# Gate A1: a material body mutation must invalidate the connection.
set +e
kprove spec-body-mutant.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTANT 2>&1 | tee "$MUTANT_RESULT_FILE"
MUTANT_STATUS="${PIPESTATUS[0]}"
set -e
if [[ "$MUTANT_STATUS" -eq 0 ]]; then
  echo "ERROR: body-mutation probe unexpectedly proved" >&2
  exit 1
fi
grep -F '"$result" |-> 1' "$MUTANT_RESULT_FILE"
echo "EXPECTED FAILURE: body-mutation probe exited $MUTANT_STATUS"
