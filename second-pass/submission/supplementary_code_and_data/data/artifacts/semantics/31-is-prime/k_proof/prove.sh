#!/usr/bin/env bash
set -euo pipefail

# Translate the submitted implementation and the concrete prompt-example
# harness with the fixed front end.
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy

# Concrete execution under the required LLVM definition.  All seven prompt
# examples are assertions; success ends with <exc> NoExc and exit code 0.
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

# Prove the general trial-divisor loop theorem from the supplied MPY rules.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-base-kompiled
kprove spec.k \
  --definition proof-base-kompiled \
  --spec-module LOOP-SPEC

# Prove both exhaustive entry branches.  For n >= 2 the prefix establishes
# divisor = 2 and reaches the source of the loop theorem above.
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
kprove spec.k \
  --definition proof-kompiled \
  --spec-module SPEC
