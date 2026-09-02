#!/usr/bin/env bash
set -euo pipefail

# Recreate the translated program from the immutable translator.
python3 py2mpy.py solution.py > solution.mpy

# The verification definition contains the semantics and the mathematical
# contract.  The Haskell backend is required by kprove.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled \
  --warnings none

# Mechanically ensure that the program named by the proof is precisely the
# freshly generated solution.mpy constructor tree.
cmp \
  <(kast solution.mpy \
      --definition verification-kompiled \
      --sort Module \
      --module VERIFICATION \
      --output kore \
      --expand-macros) \
  <(kast \
      --expression solutionProgram \
      --definition verification-kompiled \
      --sort Module \
      --module VERIFICATION \
      --output kore \
      --expand-macros)

# Concrete semantic executions: prompt example, negative even values, and
# the one-element base case.
task_example_output="$(krun solution.mpy \
  -cINPUT='pyList(cons(4, cons(2, cons(6, cons(7, nil)))))' \
  --definition verification-kompiled)"
printf '%s\n' "$task_example_output"
grep -Fq 'pyInt ( 2 )' <<<"$task_example_output"

task_negative_output="$(krun solution.mpy \
  -cINPUT='pyList(cons(-1, cons(-2, cons(-3, cons(-4, cons(-5, nil))))))' \
  --definition verification-kompiled)"
printf '%s\n' "$task_negative_output"
grep -Fq 'pyInt ( -6 )' <<<"$task_negative_output"

task_singleton_output="$(krun solution.mpy \
  -cINPUT='pyList(cons(1, nil))' \
  --definition verification-kompiled)"
printf '%s\n' "$task_singleton_output"
grep -Fq 'pyInt ( 0 )' <<<"$task_singleton_output"

# Proves every claim in spec.k.  Success prints #Top and exits zero.
kprove spec.k \
  --definition verification-kompiled \
  --warnings none
