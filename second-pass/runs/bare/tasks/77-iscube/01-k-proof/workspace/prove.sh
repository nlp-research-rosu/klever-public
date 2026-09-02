#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Translate the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Build and exercise the concrete semantics on every example in prompt.py.
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm

check_krun() {
  local input="$1"
  local expected="$2"
  local output
  output="$(krun solution.mpy -cN="$input" --definition semantic-kompiled)"
  rg -q "BoolVal \\( $expected \\)" <<<"$output"
  printf 'krun iscube(%s) = %s\n' "$input" "$expected"
}

check_krun 1 true
check_krun 2 false
check_krun -1 true
check_krun 64 true
check_krun 0 true
check_krun 180 false

# Exact cubes: prove the small-step loop invariant and both input signs.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  -o cube-verification-kompiled
kprove spec.k \
  --definition cube-verification-kompiled \
  --spec-module CUBE-SPEC

# Non-cubes: prove the open-interval loop invariant and both input signs.
kompile verification.k \
  --main-module GAP-VERIFICATION \
  --syntax-module GAP-VERIFICATION \
  --backend haskell \
  -o gap-verification-kompiled
kprove spec.k \
  --definition gap-verification-kompiled \
  --spec-module GAP-SPEC
