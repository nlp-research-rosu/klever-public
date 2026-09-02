#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/132-is-nested-review || exit 90

run_or_stop() {
  echo "\$ $*"
  "$@"
  local status=$?
  echo "EXIT_STATUS: ${status}"
  if [ "${status}" -ne 0 ]; then
    exit "${status}"
  fi
}

run_or_stop python3 /audit-output/evidence/compare_concrete_ast.py

run_or_stop kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-fresh

echo '$ python3 py2mpy.py /audit-output/evidence/auditor_concrete_tests.py > auditor_concrete_tests.mpy'
python3 py2mpy.py /audit-output/evidence/auditor_concrete_tests.py \
  > auditor_concrete_tests.mpy
translate_status=$?
echo "EXIT_STATUS: ${translate_status}"
if [ "${translate_status}" -ne 0 ]; then
  exit "${translate_status}"
fi

run_or_stop krun auditor_concrete_tests.mpy \
  --definition runtime-kompiled-fresh

run_or_stop kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-fresh

run_or_stop kprove spec.k \
  --definition verification-kompiled-fresh \
  --spec-module SPEC \
  --claims SPEC.loop

# The entry claim uses SPEC.loop as a circularity, so the complete module is
# the independent positive command for SPEC.program and also rechecks loop.
run_or_stop kprove spec.k \
  --definition verification-kompiled-fresh \
  --spec-module SPEC
