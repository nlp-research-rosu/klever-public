#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruct || exit 99
audit_overall_status=0

record_status() {
  audit_command_status=$1
  echo "EXIT_STATUS: ${audit_command_status}"
  if (( audit_command_status != 0 )); then
    audit_overall_status=1
  fi
}

echo 'COMMAND: kompile --version'
kompile --version
record_status $?

echo 'COMMAND: kprove --version'
kprove --version
record_status $?

echo 'COMMAND: python3 /reference/py2mpy.py solution.py > solution.fresh.mpy'
python3 /reference/py2mpy.py solution.py > solution.fresh.mpy
record_status $?

echo 'COMMAND: cmp -s solution.fresh.mpy solution.mpy'
cmp -s solution.fresh.mpy solution.mpy
record_status $?

echo 'COMMAND: python3 /reference/py2mpy.py concrete-tests.py > concrete-tests.fresh.mpy'
python3 /reference/py2mpy.py concrete-tests.py > concrete-tests.fresh.mpy
record_status $?

echo 'COMMAND: cmp -s concrete-tests.fresh.mpy concrete-tests.mpy'
cmp -s concrete-tests.fresh.mpy concrete-tests.mpy
record_status $?

echo 'COMMAND: kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
record_status $?

echo 'COMMAND: krun concrete-tests.fresh.mpy --definition runtime-kompiled'
krun concrete-tests.fresh.mpy --definition runtime-kompiled
record_status $?

echo 'COMMAND: kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition verification-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
record_status $?

echo 'COMMAND: kprove --definition verification-kompiled spec.k --spec-module LOOP-SPEC'
kprove \
  --definition verification-kompiled \
  spec.k \
  --spec-module LOOP-SPEC
record_status $?

echo 'COMMAND: kompile verification.k --backend haskell --main-module VERIFICATION-WITH-LOOP --syntax-module VERIFICATION-WITH-LOOP --output-definition function-verification-kompiled'
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-WITH-LOOP \
  --syntax-module VERIFICATION-WITH-LOOP \
  --output-definition function-verification-kompiled
record_status $?

echo 'COMMAND: kprove --definition function-verification-kompiled spec.k --spec-module FUNCTION-SPEC'
kprove \
  --definition function-verification-kompiled \
  spec.k \
  --spec-module FUNCTION-SPEC
record_status $?

exit "${audit_overall_status}"
