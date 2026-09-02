#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor AST and check the Python implementation.
python3 py2mpy.py solution.py > solution.mpy
python3 -m py_compile solution.py

# Concrete execution uses the fast LLVM backend.  Each Run term embeds the
# freshly regenerated solution.mpy, so these are executions of the delivered
# translated program rather than a hand-written surrogate.
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm

run_case() {
  local input="$1"
  local expected="$2"
  local program
  local output
  program="Run($(tr '\n' ' ' < solution.mpy), \"correct_bracketing\", \"${input}\")"
  output="$(krun --definition semantic-kompiled -cPGM="${program}" --output pretty)"
  printf '%s\n' "${output}"
  printf '%s\n' "${output}" | grep -q "boolVal ( ${expected} )"
}

run_case "(" false
run_case "()" true
run_case "(()())" true
run_case ")(()" false

# The Haskell backend proves the symbolic loop invariant first.  The second
# command proves every claim, using that exact already-proved invariant as a
# lemma; both required positive proof commands must print #Top and exit zero.
kompile verification.k --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell
kprove spec.k --definition verification-kompiled --spec-module SPEC -I . \
  --claims SPEC.loop
kprove spec.k --definition verification-kompiled --spec-module SPEC -I . \
  --trusted SPEC.loop
