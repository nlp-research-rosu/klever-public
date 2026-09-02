#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Recreate the submitted constructor term from the unmodified translator.
python3 py2mpy.py solution.py > solution.mpy

# Compile and exercise the concrete small-step semantics on the prompt case,
# the empty boundary, and an all-negative case.
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition semantic-kompiled

python3 make_case.py 1 2 3 2 3 4 2 > case-prompt.mpy
python3 make_case.py > case-empty.mpy
python3 make_case.py -5 -9 -3 -4 > case-negative.mpy

krun case-prompt.mpy --definition semantic-kompiled --output pretty
krun case-empty.mpy --definition semantic-kompiled --output pretty
krun case-negative.mpy --definition semantic-kompiled --output pretty

# Prove the same cases using only the operational rules in semantic.k.
kompile solution-ast.k \
  --main-module SOLUTION-AST \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition operational-kompiled
kprove operational-spec.k \
  --definition operational-kompiled \
  --spec-module OPERATIONAL-SPEC \
  --output pretty

# Prove every claim in spec.k, including the arbitrary-list theorem.
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --output pretty

# Negative validation: the mutant omits `first = False`, so its purported
# correctness claim must be rejected. A successful mutant proof fails this run.
if kprove mutation-spec.k \
     --definition verification-kompiled \
     --spec-module MUTATION-SPEC \
     --output pretty; then
  echo "ERROR: mutation unexpectedly proved" >&2
  exit 1
else
  echo "Expected mutation rejection observed"
fi
