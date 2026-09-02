#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh || exit 90
overall=0

run() {
  echo "$ $*"
  "$@"
  status=$?
  echo "exit_status=$status"
  if (( status != 0 )); then
    overall=1
  fi
}

echo '$ test ! -e runtime-kompiled && test ! -e verification-kompiled'
test ! -e runtime-kompiled && test ! -e verification-kompiled
status=$?
echo "exit_status=$status"
if (( status != 0 )); then
  exit 91
fi

run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

run krun concrete-tests.mpy \
  --definition runtime-kompiled

run kompile verification.k \
  --backend haskell \
  --main-module HOW-MANY-TIMES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

run kprove spec.k \
  --definition verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC

run kprove spec-acc.k \
  --definition verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC-ACC

run kprove spec-entry.k \
  --definition verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC-ENTRY

exit "$overall"
