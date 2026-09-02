#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/candidate-fresh
llvm_definition="$scratch/semantic-llvm-kompiled"
haskell_definition="$scratch/verification-haskell-kompiled"

for output in "$llvm_definition" "$haskell_definition"; do
  if [[ -e "$output" || -L "$output" ]]; then
    echo "ERROR: clean-build output already exists: $output"
    exit 2
  fi
done

echo 'COMMAND: kompile --backend llvm semantic.k --main-module MPY --syntax-module MPY-SYNTAX --output-definition semantic-llvm-kompiled'
(
  cd "$scratch" &&
  kompile \
    --backend llvm \
    semantic.k \
    --main-module MPY \
    --syntax-module MPY-SYNTAX \
    --output-definition semantic-llvm-kompiled
) 2>&1 | tee /audit-output/evidence/stage3/llvm-build.log
llvm_status=${PIPESTATUS[0]}
echo "LLVM_BUILD_EXIT_STATUS=$llvm_status" | tee -a /audit-output/evidence/stage3/llvm-build.log
if [[ "$llvm_status" -ne 0 ]]; then
  exit "$llvm_status"
fi

echo 'COMMAND: python3 /audit-output/evidence/stage3/concrete_semantics_compare.py'
python3 /audit-output/evidence/stage3/concrete_semantics_compare.py \
  2>&1 | tee /audit-output/evidence/stage3/concrete-semantics.log
concrete_status=${PIPESTATUS[0]}
echo "CONCRETE_COMPARE_EXIT_STATUS=$concrete_status" \
  | tee -a /audit-output/evidence/stage3/concrete-semantics.log
if [[ "$concrete_status" -ne 0 ]]; then
  exit "$concrete_status"
fi

echo 'COMMAND: kompile --backend haskell semantic.k --main-module MPY --syntax-module MPY-SYNTAX --output-definition verification-haskell-kompiled'
(
  cd "$scratch" &&
  kompile \
    --backend haskell \
    semantic.k \
    --main-module MPY \
    --syntax-module MPY-SYNTAX \
    --output-definition verification-haskell-kompiled
) 2>&1 | tee /audit-output/evidence/stage3/haskell-build.log
haskell_status=${PIPESTATUS[0]}
echo "HASKELL_BUILD_EXIT_STATUS=$haskell_status" \
  | tee -a /audit-output/evidence/stage3/haskell-build.log
if [[ "$haskell_status" -ne 0 ]]; then
  exit "$haskell_status"
fi

claim_count=$(rg -c '^[[:space:]]*claim([[:space:]]|$)' "$scratch/spec.k")
echo "POSITIVE_CLAIM_COUNT=$claim_count"
if [[ "$claim_count" -ne 1 ]]; then
  echo "ERROR: expected exactly one positive claim"
  exit 3
fi

echo 'COMMAND: kprove spec.k --definition verification-haskell-kompiled --spec-module SPEC'
(
  cd "$scratch" &&
  kprove \
    spec.k \
    --definition verification-haskell-kompiled \
    --spec-module SPEC
) 2>&1 | tee /audit-output/evidence/stage3/positive-claim.log
proof_status=${PIPESTATUS[0]}
echo "POSITIVE_PROOF_EXIT_STATUS=$proof_status" \
  | tee -a /audit-output/evidence/stage3/positive-claim.log
top_count=$(rg -c '^#Top$' /audit-output/evidence/stage3/positive-claim.log || true)
echo "POSITIVE_PROOF_TOP_COUNT=$top_count" \
  | tee -a /audit-output/evidence/stage3/positive-claim.log
if [[ "$proof_status" -ne 0 || "$top_count" -lt 1 ]]; then
  exit 4
fi

exit 0
