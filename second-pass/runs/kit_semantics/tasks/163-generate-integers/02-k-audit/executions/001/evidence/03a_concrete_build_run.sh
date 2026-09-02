#!/usr/bin/env bash
set -uo pipefail

WORK=/tmp/audit-work/reconstruction

record_status() {
  local label="$1"
  local status="$2"
  printf 'STATUS [%s]: %s\n' "$label" "$status"
  if [[ "$status" -ne 0 ]]; then
    exit "$status"
  fi
}

cd "$WORK" || exit 1

printf '%s\n' \
  'COMMAND: python3 /reference/py2mpy.py audit-concrete.py > audit-concrete.mpy'
python3 /reference/py2mpy.py audit-concrete.py > audit-concrete.mpy
status=$?
record_status "translate reviewer concrete harness" "$status"

printf '%s\n' \
  'COMMAND: python3 audit-concrete.py'
python3 audit-concrete.py
status=$?
record_status "CPython concrete harness" "$status"

printf '%s\n' \
  'COMMAND: kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition fresh-llvm-kompiled'
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-llvm-kompiled
status=$?
record_status "fresh LLVM kompile" "$status"

printf '%s\n' \
  'COMMAND: krun audit-concrete.mpy --definition fresh-llvm-kompiled'
krun audit-concrete.mpy --definition fresh-llvm-kompiled
status=$?
record_status "fresh LLVM concrete execution" "$status"

printf '%s\n' 'RESULT: fresh concrete build and execution passed'
