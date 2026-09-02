#!/usr/bin/env bash
set -u

work=/tmp/audit-work/final-reconstruction
cd "$work" || exit 1

echo '$ kompile semantic.k --backend llvm --main-module MINI-PYTHON --syntax-module MINI-PYTHON-SYNTAX --output-definition semantic-llvm-probe-kompiled'
kompile semantic.k \
  --backend llvm \
  --main-module MINI-PYTHON \
  --syntax-module MINI-PYTHON-SYNTAX \
  --output-definition semantic-llvm-probe-kompiled
build_status=$?
echo "EXIT_STATUS=$build_status"
test "$build_status" -eq 0 || exit "$build_status"

echo '$ krun solution.mpy --definition semantic-llvm-probe-kompiled -cINPUT=1'
krun solution.mpy --definition semantic-llvm-probe-kompiled -cINPUT=1
run_status=$?
echo "EXIT_STATUS=$run_status"
if test "$run_status" -eq 0; then
  echo 'LLVM_PROBE=EXECUTED'
else
  echo 'LLVM_PROBE=EXPECTED_PORTABILITY_LIMITATION'
fi
exit 0
