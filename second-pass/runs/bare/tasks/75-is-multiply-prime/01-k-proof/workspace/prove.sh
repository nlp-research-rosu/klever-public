#!/usr/bin/env bash
set -euo pipefail

# Recreate the fixed translator output and ensure it is exactly the program
# term embedded by solution-program.k.
python3 py2mpy.py solution.py > solution.mpy
printf '%s  %s\n' \
  '2ed20f37c9f9cc534ea932248a2599788f3e6de80cc7303669d627aef0439709' \
  'solution.mpy' | sha256sum --check --status

# Build the hand-written semantics plus its verification helpers.
kompile definition.k \
  --backend haskell \
  --main-module DEFINITION \
  --syntax-module MPY-SYNTAX

# Exercise positive, negative, boundary, and out-of-domain inputs.
krun solution.mpy --definition definition-kompiled -cARG=30
krun solution.mpy --definition definition-kompiled -cARG=10
krun solution.mpy --definition definition-kompiled -cARG=99
krun solution.mpy --definition definition-kompiled -cARG=-7

# This is the required positive target proof.  The explicit check makes any
# non-#Top result fail the script even if a backend ever exits successfully.
proof_output="$({
  kprove spec.k \
    --definition definition-kompiled \
    --spec-module SPEC
})"
printf '%s\n' "$proof_output"
[[ "$proof_output" == '#Top' ]]
