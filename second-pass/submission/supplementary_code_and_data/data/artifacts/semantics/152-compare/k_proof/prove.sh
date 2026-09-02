#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate both translated programs from their Python sources.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Required concrete LLVM definition and end-to-end executions.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Universal proof (the first claim in spec.k) plus the prompt-example claims.
kompile verification.k \
  --backend haskell \
  --main-module COMPARE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module COMPARE-SPEC

# Independent raw-semantics proofs: COMPARE-COMMON excludes the symbolic loop
# summary, so all four finite cases traverse the actual iterator and loop.
kompile verification.k \
  --backend haskell \
  --main-module COMPARE-COMMON \
  --syntax-module MPY-SYNTAX \
  --output-definition operational-kompiled
kprove operational-spec.k \
  --definition operational-kompiled \
  --spec-module COMPARE-OPERATIONAL-SPEC

# Negative validation: changing subtraction to addition must not prove.
mutation_log="$(mktemp)"
trap 'rm -f "$mutation_log"' EXIT
if kprove mutation-spec.k \
    --definition verification-kompiled \
    --spec-module COMPARE-MUTATION-SPEC \
    >"$mutation_log" 2>&1; then
  cat "$mutation_log"
  echo "ERROR: the deliberately incorrect addition mutant unexpectedly proved" >&2
  exit 1
fi
cat "$mutation_log"
echo "Expected result: the addition mutation was rejected."
