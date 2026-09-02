#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/reconstruction

test ! -e runtime-fresh-kompiled
test ! -e verification-fresh-kompiled

python3 py2mpy.py concrete-witness.py > concrete-witness.mpy

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-fresh-kompiled

krun concrete-witness.mpy \
  --definition runtime-fresh-kompiled \
  > /audit-output/evidence/03-krun-concrete-witness.log
krun_status=$?
printf 'krun_concrete_witness_exit=%s\n' "${krun_status}"
rg -n '<k>|<exc>|<exit-code>' \
  /audit-output/evidence/03-krun-concrete-witness.log

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled

kprove spec.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-inv \
  > /audit-output/evidence/03-kprove-loop.log 2>&1
loop_status=$?
printf 'kprove_loop_exit=%s\n' "${loop_status}"
rg -n '^#Top$|WarnStuckClaimState|\\[Error\\]' \
  /audit-output/evidence/03-kprove-loop.log

kprove spec.k \
  --definition verification-fresh-kompiled \
  --spec-module SPEC \
  > /audit-output/evidence/03-kprove-all-claims.log 2>&1
all_status=$?
printf 'kprove_all_claims_exit=%s\n' "${all_status}"
rg -n '^#Top$|WarnStuckClaimState|\\[Error\\]' \
  /audit-output/evidence/03-kprove-all-claims.log
