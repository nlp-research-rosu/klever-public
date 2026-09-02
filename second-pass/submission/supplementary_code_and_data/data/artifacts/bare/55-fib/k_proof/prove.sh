#!/usr/bin/env bash
set -euo pipefail

# Regenerate the constructor term from the submitted Python implementation.
python3 py2mpy.py solution.py > solution.mpy

# Sanity-check CPython behavior against the prompt examples and base cases.
python3 - <<'PY'
from solution import fib

for n, expected in [(0, 0), (1, 1), (2, 1), (8, 21), (10, 55)]:
    actual = fib(n)
    assert actual == expected, (n, actual, expected)
    print(f"CPython: fib({n}) = {actual}")
PY

# Compile the hand-written semantics together with the mathematical oracle.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

# Exercise the translated program in the K semantics.
run_case() {
  local n="$1"
  local expected="$2"
  local output
  output="$(krun solution.mpy -d verification-kompiled -cARG="$n" --output pretty)"
  printf '%s\n' "$output"
  grep -Fq "    $expected ~> .K" <<<"$output"
  echo "K: fib($n) = $expected"
}

run_case 0 0
run_case 1 1
run_case 2 1
run_case 8 21
run_case 10 55

# Positive target proof 1: independently prove the recursive invocation lemma.
kprove spec.k \
  -d verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.fib-invoke \
  --output pretty 2>&1 | tee kprove-invoke.out
grep -qx '#Top' kprove-invoke.out

# Positive target proof 2: prove the full spec, including the exact module.
kprove spec.k \
  -d verification-kompiled \
  --spec-module SPEC \
  --output pretty 2>&1 | tee kprove-module.out
grep -qx '#Top' kprove-module.out

# Negative validation: an off-by-one postcondition must not prove.
if kprove mutation-spec.k \
    -d verification-kompiled \
    --spec-module MUTATION-SPEC \
    --output pretty 2>&1 | tee kprove-mutation.out; then
  echo "ERROR: the deliberately false mutation unexpectedly proved" >&2
  exit 1
else
  echo "Expected failure: the off-by-one mutation was rejected"
fi
