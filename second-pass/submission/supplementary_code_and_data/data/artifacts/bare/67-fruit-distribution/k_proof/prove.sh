#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

PROVE_TMP_DIR="$(mktemp -d)"
trap 'rm -rf -- "$PROVE_TMP_DIR"' EXIT

# Reproduce the required translation and reject a stale solution.mpy.
python3 py2mpy.py solution.py > "$PROVE_TMP_DIR/solution.mpy"
cmp solution.mpy "$PROVE_TMP_DIR/solution.mpy"

# Check that the translated source is accepted and executable by the base
# semantics, independently of the verification driver.
kompile semantic.k \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend haskell
krun solution.mpy --definition semantic-kompiled --output pretty

# Compile the proof driver.  Its solutionProgram macro is checked against the
# parsed solution.mpy below, so the proof cannot silently use a different AST.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell
krun solution.mpy \
  --definition verification-kompiled \
  --depth 0 \
  --output kast \
  > "$PROVE_TMP_DIR/source.kast" 2> /dev/null
krun solution-alias.mpy \
  --definition verification-kompiled \
  --depth 0 \
  --output kast \
  > "$PROVE_TMP_DIR/alias.kast" 2> /dev/null
cmp "$PROVE_TMP_DIR/source.kast" "$PROVE_TMP_DIR/alias.kast"

run_and_expect() {
  local input_file="$1"
  local expected="$2"
  local output

  output="$(krun "$input_file" --definition verification-kompiled --output pretty)"
  printf '%s\n' "$output"
  [[ "$output" == *"VInt ( $expected )"* ]]
  [[ "$output" != *"#Bottom"* ]]
}

run_and_expect example-abstract.mpy 8
run_and_expect example-concrete-1.mpy 8
run_and_expect example-concrete-2.mpy 2
run_and_expect example-concrete-3.mpy 95
run_and_expect example-concrete-4.mpy 19

# Positive target-proof command: proves every claim in spec.k.
kprove spec.k --definition verification-kompiled --spec-module SPEC
