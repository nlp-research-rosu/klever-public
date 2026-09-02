#!/usr/bin/env bash
set -u

work=/tmp/audit-work/48-is-palindrome-audit
cd "$work" || exit 90

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS=%s\n' "$status"
  return "$status"
}

if [[ -e runtime-review4-kompiled || -L runtime-review4-kompiled ]]; then
  printf 'ERROR: runtime-review4-kompiled pre-existed\n'
  exit 91
fi
if [[ -e verification-review4-kompiled || -L verification-review4-kompiled ]]; then
  printf 'ERROR: verification-review4-kompiled pre-existed\n'
  exit 92
fi

run kompile --version || exit $?
run kprove --version || exit $?
run python3 -m py_compile runtime-audit.py py2mpy.py || exit $?
run kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-review4-kompiled || exit $?
run bash -c 'python3 py2mpy.py runtime-audit.py > runtime-audit.mpy' || exit $?
run krun runtime-audit.mpy \
  --definition runtime-review4-kompiled || exit $?
run kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-review4-kompiled || exit $?

printf 'POSITIVE_CLAIM_INVENTORY:\n'
rg -n '^[[:space:]]*claim([[:space:]]|\[)' spec.k
claim_count="$(rg -c '^[[:space:]]*claim([[:space:]]|\[)' spec.k)"
printf 'POSITIVE_CLAIM_COUNT=%s\n' "$claim_count"
if [[ "$claim_count" != 1 ]]; then
  printf 'ERROR: expected exactly one positive target claim\n'
  exit 93
fi

run kprove spec.k \
  --definition verification-review4-kompiled \
  --spec-module SPEC \
  --claims SPEC.is-palindrome || exit $?

printf 'RECONSTRUCTION_RESULT=PASS\n'
