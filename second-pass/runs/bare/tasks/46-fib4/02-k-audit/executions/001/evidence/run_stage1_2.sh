#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return "$status"
}

scratch=/tmp/audit-work/46-fib4

printf 'AUDIT STAGES 1-2: provenance, clean source copy, translation, differential\n'
run find /reference -maxdepth 2 -printf '%y %p -> %l\n'
run test ! -e /reference/reference-semantics
run test ! -L /reference/reference-semantics
run find /candidate -maxdepth 1 -printf '%y %f -> %l\n'
run stat -c '%F %n' \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /candidate/solution.py \
  /candidate/solution.mpy \
  /candidate/semantic.k \
  /candidate/verification.k \
  /candidate/spec.k \
  /candidate/prove.sh
run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json
run sha256sum \
  /reference/prompt.py \
  /candidate/prompt.py \
  /reference/py2mpy.py \
  /candidate/py2mpy.py \
  /candidate/run-input.json \
  /candidate/metrics.json \
  /candidate/codex-last.txt \
  /candidate/codex-output.log
run cmp /reference/prompt.py /candidate/prompt.py
run cmp /reference/py2mpy.py /candidate/py2mpy.py

run mkdir -p "$scratch"
run cp /candidate/solution.py "$scratch/solution.py"
run cp /candidate/solution.mpy "$scratch/submitted-solution.mpy"
run cp /candidate/semantic.k "$scratch/semantic.k"
run cp /candidate/verification.k "$scratch/verification.k"
run cp /candidate/spec.k "$scratch/spec.k"
run cp /reference/py2mpy.py "$scratch/trusted-py2mpy.py"
run python3 "$scratch/trusted-py2mpy.py" "$scratch/solution.py"

# The translator writes to stdout; this second invocation is intentionally
# captured as the scratch source artifact used by the build.
printf '\nCOMMAND: python3 %q %q > %q\n' \
  "$scratch/trusted-py2mpy.py" "$scratch/solution.py" "$scratch/solution.mpy"
python3 "$scratch/trusted-py2mpy.py" "$scratch/solution.py" > "$scratch/solution.mpy"
status=$?
printf 'EXIT: %d\n' "$status"

run sha256sum "$scratch/solution.mpy" "$scratch/submitted-solution.mpy"
run cmp "$scratch/solution.mpy" "$scratch/submitted-solution.mpy"
run python3 /audit-output/evidence/differential_test.py
