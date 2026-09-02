#!/usr/bin/env bash
set -uo pipefail
cd /tmp/audit-work

echo 'COMMAND: kompile trusted supplied semantics (LLVM)'
echo 'kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition replay-runtime-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition replay-runtime-kompiled
llvm_status=$?
echo "EXIT: $llvm_status"

echo 'COMMAND: krun submitted solution module'
echo 'krun submitted-solution.mpy --definition replay-runtime-kompiled'
krun submitted-solution.mpy --definition replay-runtime-kompiled
solution_status=$?
echo "EXIT: $solution_status"

echo 'COMMAND: krun reviewer normal/boundary assertions'
echo 'krun reviewer-concrete-checks.mpy --definition replay-runtime-kompiled'
krun reviewer-concrete-checks.mpy --definition replay-runtime-kompiled
checks_status=$?
echo "EXIT: $checks_status"

echo 'COMMAND: kompile proof definition (Haskell)'
echo 'kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition replay-verification-kompiled'
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition replay-verification-kompiled
haskell_status=$?
echo "EXIT: $haskell_status"

exit $((llvm_status || solution_status || checks_status || haskell_status))
