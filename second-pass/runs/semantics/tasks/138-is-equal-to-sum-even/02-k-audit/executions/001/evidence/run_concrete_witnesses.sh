#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/review-138
evidence=/audit-output/evidence
cd "$work" || exit 99

run_logged() {
  local log="$1"
  shift
  {
    printf 'WORKDIR: %s\n' "$PWD"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    status=$?
    printf 'EXIT_STATUS: %s\n' "$status"
    exit "$status"
  } 2>&1 | tee "$evidence/$log"
  return "${PIPESTATUS[0]}"
}

echo "COMMAND: python3 /reference/py2mpy.py runtime-witnesses.py"
python3 /reference/py2mpy.py runtime-witnesses.py > runtime-witnesses.mpy
translate_status=$?
echo "EXIT_STATUS: $translate_status"

if [[ "$translate_status" -ne 0 ]]; then
  exit "$translate_status"
fi

run_logged build-runtime.log \
  kompile reference-semantics/semantics.k \
    --backend llvm \
    --main-module MPY-KRUN \
    --syntax-module MPY-SYNTAX \
    --output-definition runtime-kompiled
build_status=$?

if [[ "$build_status" -ne 0 ]]; then
  exit "$build_status"
fi

run_logged run-runtime-witnesses.log \
  krun runtime-witnesses.mpy \
    --definition runtime-kompiled
runtime_status=$?

echo "COMMAND: python3 /audit-output/evidence/claim_witnesses.py"
python3 /audit-output/evidence/claim_witnesses.py
python_status=$?
echo "EXIT_STATUS: $python_status"

if [[ "$runtime_status" -ne 0 || "$python_status" -ne 0 ]]; then
  exit 1
fi
