#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/58-common

echo 'COMMAND: kompile --version; kprove --version; krun --version'
kompile --version
kprove --version
krun --version
version_status=$?
echo "EXIT: ${version_status}"

echo 'COMMAND: python3 py2mpy.py /audit-output/evidence/concrete_audit.py > concrete-audit.mpy'
python3 py2mpy.py /audit-output/evidence/concrete_audit.py > concrete-audit.mpy
translate_status=$?
echo "EXIT: ${translate_status}"

echo 'COMMAND: kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled'
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
llvm_build_status=$?
echo "EXIT: ${llvm_build_status}"

echo 'COMMAND: krun concrete-audit.mpy --definition runtime-audit-kompiled'
krun concrete-audit.mpy --definition runtime-audit-kompiled
krun_status=$?
echo "EXIT: ${krun_status}"

echo 'COMMAND: kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled'
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
haskell_build_status=$?
echo "EXIT: ${haskell_build_status}"

claims=(member-fold common-loop common-program)
proof_failure=0
for claim in "${claims[@]}"; do
  echo "COMMAND: kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --claims SPEC.${claim}"
  kprove spec.k \
    --definition verification-audit-kompiled \
    --spec-module SPEC \
    --claims "SPEC.${claim}"
  claim_status=$?
  echo "CLAIM ${claim} EXIT: ${claim_status}"
  if [[ ${claim_status} -ne 0 ]]; then
    proof_failure=1
  fi
done

echo "SUMMARY version=${version_status} translate=${translate_status} llvm_build=${llvm_build_status} krun=${krun_status} haskell_build=${haskell_build_status} proof_failure=${proof_failure}"
if [[ ${version_status} -ne 0 || ${translate_status} -ne 0 || ${llvm_build_status} -ne 0 || ${krun_status} -ne 0 || ${haskell_build_status} -ne 0 || ${proof_failure} -ne 0 ]]; then
  exit 1
fi
