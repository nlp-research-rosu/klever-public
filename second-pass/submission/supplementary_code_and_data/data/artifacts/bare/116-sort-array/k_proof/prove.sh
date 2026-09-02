#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the translated constructor term and reject syntax drift.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

# verification.k imports semantic.k; this produces one definition used by
# concrete execution, KORE-level source linkage, and proof.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --warnings none

# Prove that solutionProgram (the compact term used in spec.k) expands to the
# exact same KORE tree as the current py2mpy.py output.
actual_kore="$(mktemp)"
named_kore="$(mktemp)"
cleanup() {
  rm -f -- "$actual_kore" "$named_kore"
}
trap cleanup EXIT

kast solution.mpy \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Pgm \
  --output kore \
  --expand-macros > "$actual_kore"
kast --expression solutionProgram \
  --definition verification-kompiled \
  --module VERIFICATION \
  --sort Pgm \
  --output kore \
  --expand-macros > "$named_kore"
cmp "$actual_kore" "$named_kore"

# Concrete executions through the semantics (including cases that distinguish
# the prose contract from ordinary numeric sorting).
krun solution.mpy \
  -cARGS='listV(1 :: 5 :: 2 :: 3 :: 4 :: .Ints)' \
  --definition verification-kompiled
krun solution.mpy \
  -cARGS='listV(1 :: 0 :: 2 :: 3 :: 4 :: .Ints)' \
  --definition verification-kompiled
krun solution.mpy \
  -cARGS='listV(3 :: 1 :: 3 :: 0 :: 1 :: .Ints)' \
  --definition verification-kompiled
krun solution.mpy \
  -cARGS='listV(-2 :: -3 :: -4 :: -5 :: -6 :: .Ints)' \
  --definition verification-kompiled

# This is the sole positive target-proof command.  It proves every claim in
# SPEC and must print #Top and exit zero.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --warnings none
