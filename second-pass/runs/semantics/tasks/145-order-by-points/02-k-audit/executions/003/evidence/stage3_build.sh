#!/usr/bin/env bash
set -u
cd /tmp/audit-work/source

run_and_record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  return 0
}

run_and_record python3 \
  /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/source/reviewer_concrete.py

printf '%s\n' 'NOTE: The preceding translator output is displayed only; the executable term was regenerated separately as reviewer_concrete.mpy.'
printf '%s\n' 'COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/source/reviewer_concrete.py > /tmp/audit-work/source/reviewer_concrete.mpy'
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/source/reviewer_concrete.py \
  > /tmp/audit-work/source/reviewer_concrete.mpy
printf 'EXIT_STATUS: %s\n' "$?"

run_and_record kompile \
  /tmp/audit-work/source/reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/source/runtime-kompiled

run_and_record krun \
  /tmp/audit-work/source/reviewer_concrete.mpy \
  --definition /tmp/audit-work/source/runtime-kompiled

run_and_record kompile \
  /tmp/audit-work/source/verification.k \
  --backend haskell \
  --main-module ORDER-BY-POINTS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/source/verification-kompiled
