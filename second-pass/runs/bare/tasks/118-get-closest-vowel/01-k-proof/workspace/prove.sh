#!/usr/bin/env bash
set -euo pipefail

proof_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$proof_dir"

# Recreate the submitted constructor term with the required fixed translator,
# then ensure the exact term proved below was mechanically derived from it.
python3 py2mpy.py solution.py > solution.mpy
python3 check_program_module.py solution.mpy program.k

kompile semantic.k \
  --backend haskell \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --warnings none

# Exercise all examples from prompt.py through the K semantics.  grep makes a
# stuck or incorrect final configuration fail this script.
krun solution.mpy -cARG='word("yogurt")' --output pretty \
  | grep -Fq 'pyStr ( snoc ( .Chars , vow ( v_u ) ) )'
krun solution.mpy -cARG='word("FULL")' --output pretty \
  | grep -Fq 'pyStr ( snoc ( .Chars , vow ( v_U ) ) )'
krun solution.mpy -cARG='word("quick")' --output pretty \
  | grep -Fq 'pyStr ( .Chars )'
krun solution.mpy -cARG='word("ab")' --output pretty \
  | grep -Fq 'pyStr ( .Chars )'

# This is the positive target proof command.  Success prints #Top.
kprove spec.k --definition semantic-kompiled --warnings none
