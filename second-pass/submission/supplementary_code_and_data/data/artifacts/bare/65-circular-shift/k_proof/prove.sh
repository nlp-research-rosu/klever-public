#!/usr/bin/env bash
set -euo pipefail

# Recreate the required constructor program from the submitted Python source.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

# Sanity-check the implementation with CPython before exercising our K semantics.
python3 - <<'PY'
from solution import circular_shift

assert circular_shift(12, 1) == "21"
assert circular_shift(12, 2) == "12"
assert circular_shift(1234, 0) == "1234"
assert circular_shift(1234, 2) == "3412"
assert circular_shift(1234, 5) == "4321"
PY

# verification.k imports semantic.k, so this compiles the semantics, proof
# vocabulary, and the parser for solution.mpy into one Haskell definition.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX

# Prove that the constructor tree mentioned by the claims is byte-for-byte the
# same canonical K AST as the freshly translated solution.mpy program.
actual_ast="$(kast --definition verification-kompiled solution.mpy)"
proof_ast="$(kast --definition verification-kompiled \
  --module VERIFICATION --sort Program \
  --expression 'solutionProgram' --expand-macros)"
if [[ "$actual_ast" != "$proof_ast" ]]; then
  echo "proof/program constructor trees differ" >&2
  exit 1
fi

run_case() {
  local x="$1"
  local shift="$2"
  local expected="$3"
  local output
  output="$(krun solution.mpy \
    --definition verification-kompiled \
    -cENTRY='"circular_shift"' \
    -cARGS="VInt($x), VInt($shift)")"
  printf '%s\n' "$output"
  grep -Fq "VString ( \"$expected\" )" <<<"$output"
}

# krun exercises equality, ordinary rotation, and oversized reversal paths.
run_case 12 1 21
run_case 12 2 12
run_case 1234 2 3412
run_case 1234 5 4321

# This is the required positive target proof. It proves every claim in spec.k
# and must print #Top and exit zero.
kprove spec.k --definition verification-kompiled
