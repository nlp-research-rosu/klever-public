#!/usr/bin/env bash
set -u
set -o pipefail

cd /tmp/audit-work/125-split-words

echo '$ kompile --version; krun --version; kprove --version'
kompile --version
krun --version
kprove --version
echo "version_commands_exit=$?"

echo '$ test ! -e audit-runtime-kompiled && test ! -e audit-verification-kompiled'
test ! -e audit-runtime-kompiled && test ! -e audit-verification-kompiled
echo "clean_output_precondition_exit=$?"

echo '$ kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
echo "llvm_kompile_exit=$?"

echo '$ krun solution.mpy --definition audit-runtime-kompiled'
krun solution.mpy --definition audit-runtime-kompiled
echo "solution_krun_exit=$?"

echo '$ python3 py2mpy.py concrete_tests.py > audit-concrete-tests.mpy'
python3 py2mpy.py concrete_tests.py > audit-concrete-tests.mpy
echo "concrete_test_translation_exit=$?"

echo '$ krun audit-concrete-tests.mpy --definition audit-runtime-kompiled'
krun audit-concrete-tests.mpy --definition audit-runtime-kompiled
echo "concrete_tests_krun_exit=$?"

echo '$ kompile verification.k --backend haskell --main-module SPLIT-WORDS-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module SPLIT-WORDS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
echo "haskell_kompile_exit=$?"

echo '$ kprove spec.k --definition audit-verification-kompiled --spec-module SPEC'
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
echo "all_claims_kprove_exit=$?"

for label in whitespace comma odd-lowercase-count; do
  echo "$ kprove spec.k --definition audit-verification-kompiled --spec-module SPEC --claims $label"
  kprove spec.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC \
    --claims "$label"
  echo "${label}_kprove_exit=$?"
done
