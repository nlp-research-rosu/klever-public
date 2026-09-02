#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the transliterated program from the immutable front end.
python3 py2mpy.py solution.py > solution.mpy

# Compile and exercise only the executable semantics (no verification lemma).
kompile semantic.k \
  --backend llvm \
  --main-module EXECUTION \
  --syntax-module MPY-SYNTAX \
  --output-definition execution-kompiled \
  -w none

run_case() {
  input=$1
  expected=$2
  case_output=$(krun solution.mpy \
    --definition execution-kompiled \
    -cINPUT="$input" \
    --color off)
  printf '%s\n' "$case_output"
  printf '%s\n' "$case_output" | grep -Fq '    true'
  printf '%s\n' "$case_output" | grep -Fq "strVal ( $expected )"
}

run_case '""' '""'
run_case '"cat"' '"catac"'
run_case '"cata"' '"catac"'
run_case '"xyx"' '"xyx"'
run_case '"abcd"' '"abcdcba"'
run_case '"aabb"' '"aabbaa"'

# Prove the concrete claims using the unaugmented interpreter.
kompile semantic.k \
  --backend haskell \
  --main-module EXECUTION \
  --syntax-module MPY-SYNTAX \
  --output-definition execution-proof-kompiled \
  -w none
kprove spec.k \
  --definition execution-proof-kompiled \
  --spec-module CONCRETE-SPEC \
  -w none

# Prove arbitrary-string equivalence using the proof-only recursive summary.
kompile semantic.k \
  --backend haskell \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled \
  -w none
kprove spec.k \
  --definition semantic-kompiled \
  --spec-module SPEC \
  -w none

# Negative probe: this deliberately false claim must fail and expose "catac".
if kprove mutation-spec.k \
     --definition execution-proof-kompiled \
     --spec-module MUTATION-SPEC \
     -w none > mutation-proof.log 2>&1; then
  echo 'ERROR: deliberately false mutation claim unexpectedly proved' >&2
  exit 1
fi
grep -Fq 'strVal ( "catac" )' mutation-proof.log
echo 'Expected-failure mutation probe rejected.'
