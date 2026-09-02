#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Regenerate the submitted constructor tree with the fixed translator.
python3 py2mpy.py solution.py > solution.mpy

# Compile the executable semantics and exercise the generated program itself.
kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm

run_case() {
  local input=$1
  local expected=$2
  local output compact

  output=$(krun \
    <(sed "1s/^/Invoke(/; \$s/\$/, \"digits\", ${input})/" solution.mpy) \
    --definition semantic-kompiled \
    --output pretty)
  printf '%s\n' "$output"
  compact=$(printf '%s' "$output" | tr -d '[:space:]')
  if [[ "$compact" != *"<answer>${expected}~>.K</answer>"* ]]; then
    printf 'unexpected answer for digits(%s): expected %s\n' \
      "$input" "$expected" >&2
    return 1
  fi
}

run_case 1 1
run_case 4 0
run_case 235 15
run_case 2468 0
run_case 13579 945
run_case 10203 3

# Compile the proof definition, including the mathematical fold functions.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell

# Check that SolutionProgram in verification.k is structurally identical to
# the newly generated solution.mpy term before using it in the proof.
program_check=$(krun \
  <(sed '1s/^/CheckProgram(SolutionProgram, /; $s/$/)/' solution.mpy) \
  --definition verification-kompiled \
  --output pretty)
printf '%s\n' "$program_check"
compact_check=$(printf '%s' "$program_check" | tr -d '[:space:]')
if [[ "$compact_check" != *'<k>ProgramsMatch~>.K</k>'* ]]; then
  printf 'solution.mpy differs from SolutionProgram in verification.k\n' >&2
  exit 1
fi

# This single positive target proves both claims in spec.k: the generalized
# loop invariant and the end-to-end result for every positive integer.
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
