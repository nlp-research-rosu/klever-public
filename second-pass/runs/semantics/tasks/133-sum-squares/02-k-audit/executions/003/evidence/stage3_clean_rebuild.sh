#!/usr/bin/env bash
set -u

work=/tmp/audit-work/candidate
cd "$work" || exit 90

run_plain() {
  printf '\n$ %s\n' "$*"
  "$@"
  local status=$?
  printf 'EXIT: %s\n' "$status"
  return "$status"
}

run_proof() {
  printf '\n$ %s\n' "$*"
  local output
  output=$("$@" 2>&1)
  local status=$?
  printf '%s\n' "$output"
  printf 'EXIT: %s\n' "$status"
  if (( status != 0 )); then
    return "$status"
  fi
  if ! grep -Fxq '#Top' <<<"$output"; then
    printf '%s\n' 'ERROR: exit 0 without an exact #Top output line'
    return 91
  fi
}

printf '\n%s\n' '$ python3 /reference/py2mpy.py concrete_tests.py > /tmp/audit-work/concrete_translate.stdout'
python3 /reference/py2mpy.py concrete_tests.py > /tmp/audit-work/concrete_translate.stdout
translate_status=$?
printf 'EXIT: %s\n' "$translate_status"
printf '%s\n' '$ cmp concrete_tests.mpy /tmp/audit-work/concrete_translate.stdout'
cmp concrete_tests.mpy /tmp/audit-work/concrete_translate.stdout
cmp_status=$?
printf 'EXIT: %s\n' "$cmp_status"
if (( translate_status != 0 || cmp_status != 0 )); then
  exit 1
fi

run_plain kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled || exit $?

run_plain krun concrete_tests.mpy \
  --definition audit-runtime-kompiled \
  --output pretty || exit $?

run_plain kompile verification.k \
  --backend haskell \
  --main-module SUM-SQUARES-VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-loop-verification-kompiled || exit $?

run_proof kprove spec.k \
  --definition audit-loop-verification-kompiled \
  --spec-module SUM-SQUARES-LOOP-SPEC \
  --claims SUM-SQUARES-LOOP-SPEC.loop-correct \
  --output pretty || exit $?

run_plain kompile verification.k \
  --backend haskell \
  --main-module SUM-SQUARES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled || exit $?

run_proof kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SUM-SQUARES-SPEC \
  --claims SUM-SQUARES-SPEC.function-correct \
  --output pretty || exit $?
