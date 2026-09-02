#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/64-vowels-count
kompile --version
kprove --version
krun --version

test ! -e audit-semantic-kompiled
test ! -e audit-verification-kompiled

kompile semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition audit-semantic-kompiled
llvm_build_status=$?
printf 'LLVM_BUILD_EXIT_STATUS=%d\n' "$llvm_build_status"

kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition audit-verification-kompiled
haskell_build_status=$?
printf 'HASKELL_BUILD_EXIT_STATUS=%d\n' "$haskell_build_status"

python3 /audit-output/evidence/k_concrete_compare.py
concrete_status=$?
printf 'CONCRETE_COMPARE_EXIT_STATUS=%d\n' "$concrete_status"

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --output pretty
all_claims_status=$?
printf 'ALL_CLAIMS_EXIT_STATUS=%d\n' "$all_claims_status"

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.program-loads-solution \
  --output pretty
loader_claim_status=$?
printf 'LOADER_CLAIM_EXIT_STATUS=%d\n' "$loader_claim_status"

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.vowels-count-correct \
  --output pretty
correctness_claim_status=$?
printf 'CORRECTNESS_CLAIM_EXIT_STATUS=%d\n' "$correctness_claim_status"

if (( llvm_build_status != 0 )); then exit "$llvm_build_status"; fi
if (( haskell_build_status != 0 )); then exit "$haskell_build_status"; fi
if (( concrete_status != 0 )); then exit "$concrete_status"; fi
if (( all_claims_status != 0 )); then exit "$all_claims_status"; fi
if (( loader_claim_status != 0 )); then exit "$loader_claim_status"; fi
if (( correctness_claim_status != 0 )); then exit "$correctness_claim_status"; fi

