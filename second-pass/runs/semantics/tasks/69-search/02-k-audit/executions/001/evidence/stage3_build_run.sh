#!/usr/bin/env bash
set -u

overall=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
  return 0
}

run_shell() {
  printf '\n$ %s\n' "$1"
  bash -o pipefail -c "$1"
  status=$?
  printf '[exit %d]\n' "$status"
  if (( status != 0 )); then
    overall=1
  fi
  return 0
}

run /usr/bin/kompile --version
run /usr/bin/kprove --version
run /usr/bin/krun --version

run_shell "python3 /reference/py2mpy.py /audit-output/evidence/concrete_smoke.py > /tmp/audit-work/69-search/concrete-smoke.mpy"

run /usr/bin/kompile \
  reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

run /usr/bin/krun \
  concrete-smoke.mpy \
  --definition runtime-kompiled \
  --output none

run /usr/bin/kompile \
  verification.k \
  --backend haskell \
  --main-module SEARCH-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

run /usr/bin/kprove \
  spec.k \
  --definition verification-kompiled \
  --spec-module SEARCH-SPEC

exit "$overall"
