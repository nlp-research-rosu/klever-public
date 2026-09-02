#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/31-is-prime-audit
cd "${work}" || exit 125

failures=0

run_checked() {
  description=$1
  shift
  echo
  echo "COMMAND (${description}):"
  printf ' %q' "$@"
  echo
  "$@"
  status=$?
  echo "EXIT_STATUS (${description}): ${status}"
  if [[ ${status} -ne 0 ]]; then
    failures=$((failures + 1))
  fi
  return 0
}

echo "WORKDIR: ${work}"
echo 'CLEAN_DEFINITION_PRECHECK:'
for path in runtime-kompiled proof-base-kompiled proof-kompiled; do
  if [[ -e ${path} ]]; then
    echo "UNEXPECTED_EXISTING_PATH: ${path}"
    failures=$((failures + 1))
  else
    echo "ABSENT_AS_REQUIRED: ${path}"
  fi
done

echo
echo 'SOURCE_MANIFEST:'
sha256sum \
  solution.py \
  solution.submitted.mpy \
  solution.regenerated.mpy \
  spec.k \
  verification.k \
  reference-semantics/semantics.k

run_checked translate-concrete \
  python3 py2mpy.py concrete_tests.py
python3 py2mpy.py concrete_tests.py > concrete_tests.regenerated.mpy
translate_write_status=$?
echo "EXIT_STATUS (write-concrete-translation): ${translate_write_status}"
if [[ ${translate_write_status} -ne 0 ]]; then
  failures=$((failures + 1))
fi

run_checked concrete-translation-byte-identity \
  cmp -s concrete_tests.regenerated.mpy concrete_tests.submitted.mpy

run_checked compile-concrete \
  timeout 900 kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-kompiled

run_checked run-concrete-examples \
  timeout 300 krun concrete_tests.regenerated.mpy \
    --definition runtime-kompiled

run_checked compile-loop-proof-definition \
  timeout 900 kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION-BASE \
    --syntax-module MPY-SYNTAX \
    --output-definition proof-base-kompiled

run_checked prove-loop-module \
  timeout 900 kprove spec.k \
    --definition proof-base-kompiled \
    --spec-module LOOP-SPEC

run_checked prove-loop-claim-alone \
  timeout 900 kprove spec.k \
    --definition proof-base-kompiled \
    --spec-module LOOP-SPEC \
    --claims LOOP-SPEC.loop-correct

run_checked compile-entry-proof-definition \
  timeout 900 kompile verification.k \
    --backend haskell \
    --main-module VERIFICATION \
    --syntax-module MPY-SYNTAX \
    --output-definition proof-kompiled

run_checked prove-entry-module \
  timeout 900 kprove spec.k \
    --definition proof-kompiled \
    --spec-module SPEC

run_checked prove-entry-small-alone \
  timeout 900 kprove spec.k \
    --definition proof-kompiled \
    --spec-module SPEC \
    --claims SPEC.entry-small

run_checked prove-entry-large-prefix-alone \
  timeout 900 kprove spec.k \
    --definition proof-kompiled \
    --spec-module SPEC \
    --claims SPEC.entry-large-prefix

echo
echo "FAILURE_COUNT: ${failures}"
if [[ ${failures} -ne 0 ]]; then
  exit 1
fi
exit 0
