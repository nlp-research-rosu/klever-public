#!/usr/bin/env bash
set -u
cd /tmp/audit-work/audit147 || exit 99
overall=0

echo '$ kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX --backend llvm --output-definition fresh-runtime-kompiled'
kompile semantic.k \
  --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition fresh-runtime-kompiled
status=$?
echo "exit_status=$status"
if [ "$status" -ne 0 ]; then overall=1; fi

echo '$ python3 /audit-output/evidence/semantic_concrete_check.py'
python3 /audit-output/evidence/semantic_concrete_check.py
status=$?
echo "exit_status=$status"
if [ "$status" -ne 0 ]; then overall=1; fi

echo '$ kompile verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --backend haskell --output-definition fresh-verification-kompiled'
kompile verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --backend haskell \
  --output-definition fresh-verification-kompiled
status=$?
echo "exit_status=$status"
if [ "$status" -ne 0 ]; then overall=1; fi

echo '$ kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC'
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC
status=$?
echo "exit_status=$status"
if [ "$status" -ne 0 ]; then overall=1; fi

echo "overall_exit_status=$overall"
exit "$overall"
