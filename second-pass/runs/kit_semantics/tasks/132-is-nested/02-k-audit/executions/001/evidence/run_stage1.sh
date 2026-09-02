#!/usr/bin/env bash
set -uo pipefail

run_and_record() {
  local label="$1"
  shift
  echo "\$ $*"
  "$@"
  local status=$?
  echo "EXIT_STATUS: ${status}"
  return "${status}"
}

run_and_record "integrity" python3 /audit-output/evidence/stage1_integrity.py
run_and_record "semantics-diff" diff --no-dereference --recursive --brief \
  /candidate/reference-semantics /reference/reference-semantics
run_and_record "prompt-cmp" cmp /candidate/prompt.py /reference/prompt.py
run_and_record "translator-cmp" cmp /candidate/py2mpy.py /reference/py2mpy.py
run_and_record "trace-inventory" python3 /audit-output/evidence/trace_inventory.py
