#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
overall=0

run_logged() {
  local label=$1
  shift
  local log="$evidence/$label.log"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" 2>&1 | tee "$log"
  local status=${PIPESTATUS[0]}
  printf 'EXIT_STATUS: %s\n' "$status" | tee -a "$log"
  if [[ $status -ne 0 ]]; then
    overall=1
  fi
  return "$status"
}

cd "$work" || exit 1

printf 'COMMAND: python3 py2mpy.py auditor-concrete-tests.py > auditor-concrete-tests.mpy\n'
python3 py2mpy.py auditor-concrete-tests.py > auditor-concrete-tests.mpy
translate_status=$?
printf 'EXIT_STATUS: %s\n' "$translate_status" | tee "$evidence/03a-concrete-translate.log"
if [[ $translate_status -ne 0 ]]; then
  exit "$translate_status"
fi

run_logged 03b-kompile-llvm \
  kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled || exit $?

run_logged 03c-krun-concrete \
  krun auditor-concrete-tests.mpy \
  --definition runtime-kompiled || exit $?

run_logged 03d-kompile-base \
  kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled || exit $?

run_logged 03e-kprove-aux \
  kprove spec.k \
  --definition verification-base-kompiled \
  --spec-module AUX-SPEC || exit $?
if ! grep -qx '#Top' "$evidence/03e-kprove-aux.log"; then
  printf 'SUCCESS_SIGNAL_MISSING: exact #Top line not found\n' |
    tee -a "$evidence/03e-kprove-aux.log"
  exit 1
fi

run_logged 03f-kompile-lemma \
  kompile verification.k \
  --backend haskell \
  --main-module MPY-VERIFICATION-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-lemma-kompiled || exit $?

run_logged 03g-kprove-main \
  kprove spec.k \
  --definition verification-lemma-kompiled \
  --spec-module MAIN-SPEC || exit $?
if ! grep -qx '#Top' "$evidence/03g-kprove-main.log"; then
  printf 'SUCCESS_SIGNAL_MISSING: exact #Top line not found\n' |
    tee -a "$evidence/03g-kprove-main.log"
  exit 1
fi

printf 'POSITIVE_RECONSTRUCTION_STATUS: %s\n' "$overall"
exit "$overall"
