#!/usr/bin/env bash
set -euo pipefail

python3 py2mpy.py solution.py > solution.mpy

kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled

true_run="$(krun solution.mpy \
  -cARGS='strVal("1/5"),strVal("5/1")' \
  --definition proof-kompiled)"
printf '%s\n' "$true_run"
grep -Fq 'result ( boolVal ( true ) )' <<<"$true_run"

false_run_one="$(krun solution.mpy \
  -cARGS='strVal("1/6"),strVal("2/1")' \
  --definition proof-kompiled)"
printf '%s\n' "$false_run_one"
grep -Fq 'result ( boolVal ( false ) )' <<<"$false_run_one"

false_run_two="$(krun solution.mpy \
  -cARGS='strVal("7/10"),strVal("10/2")' \
  --definition proof-kompiled)"
printf '%s\n' "$false_run_two"
grep -Fq 'result ( boolVal ( false ) )' <<<"$false_run_two"

proof_output="$(kprove spec.k --definition proof-kompiled)"
printf '%s\n' "$proof_output"
test "$proof_output" = '#Top'
