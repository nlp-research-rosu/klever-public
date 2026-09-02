#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/reconstruction
cd "$scratch" || exit 90

echo "COMMAND kompile --version"
kompile --version
echo "KOMPILE_VERSION_EXIT=$?"
echo "COMMAND kprove --version"
kprove --version
echo "KPROVE_VERSION_EXIT=$?"
echo "COMMAND krun --version"
krun --version
echo "KRUN_VERSION_EXIT=$?"

echo "COMMAND find $scratch -maxdepth 1 -type d -name '*-kompiled' -print"
find "$scratch" -maxdepth 1 -type d -name '*-kompiled' -print
echo "PREBUILD_CACHE_CHECK_EXIT=$?"

echo "COMMAND python3 py2mpy.py audit-concrete.py > audit-concrete.mpy"
python3 py2mpy.py audit-concrete.py > audit-concrete.mpy
translate_status=$?
echo "CONCRETE_TRANSLATE_EXIT=$translate_status"

echo "COMMAND kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled"
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
runtime_build_status=$?
echo "RUNTIME_KOMPILE_EXIT=$runtime_build_status"

runtime_solution_status=99
runtime_tests_status=99
if [[ $runtime_build_status -eq 0 ]]; then
  echo "COMMAND krun solution.mpy --definition runtime-kompiled"
  krun solution.mpy --definition runtime-kompiled
  runtime_solution_status=$?
  echo "SOLUTION_KRUN_EXIT=$runtime_solution_status"

  echo "COMMAND krun audit-concrete.mpy --definition runtime-kompiled"
  krun audit-concrete.mpy --definition runtime-kompiled
  runtime_tests_status=$?
  echo "CONCRETE_TEST_KRUN_EXIT=$runtime_tests_status"
fi

echo "COMMAND kompile verification.k --backend haskell --main-module MEDIAN-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled"
kompile verification.k \
  --backend haskell \
  --main-module MEDIAN-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
proof_build_status=$?
echo "VERIFICATION_KOMPILE_EXIT=$proof_build_status"

odd_status=99
even_status=99
combined_status=99
if [[ $proof_build_status -eq 0 ]]; then
  echo "COMMAND kprove spec.k --definition verification-kompiled --spec-module MEDIAN-SPEC --claims median-odd"
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module MEDIAN-SPEC \
    --claims median-odd
  odd_status=$?
  echo "ODD_KPROVE_EXIT=$odd_status"

  echo "COMMAND kprove spec.k --definition verification-kompiled --spec-module MEDIAN-SPEC --claims median-even"
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module MEDIAN-SPEC \
    --claims median-even
  even_status=$?
  echo "EVEN_KPROVE_EXIT=$even_status"

  echo "COMMAND kprove spec.k --definition verification-kompiled --spec-module MEDIAN-SPEC"
  kprove spec.k \
    --definition verification-kompiled \
    --spec-module MEDIAN-SPEC
  combined_status=$?
  echo "COMBINED_KPROVE_EXIT=$combined_status"
fi

echo "SUMMARY translate=$translate_status runtime_build=$runtime_build_status runtime_solution=$runtime_solution_status runtime_tests=$runtime_tests_status proof_build=$proof_build_status odd=$odd_status even=$even_status combined=$combined_status"

if [[ $translate_status -eq 0 &&
      $runtime_build_status -eq 0 &&
      $runtime_solution_status -eq 0 &&
      $runtime_tests_status -eq 0 &&
      $proof_build_status -eq 0 &&
      $odd_status -eq 0 &&
      $even_status -eq 0 &&
      $combined_status -eq 0 ]]; then
  exit 0
fi
exit 1
