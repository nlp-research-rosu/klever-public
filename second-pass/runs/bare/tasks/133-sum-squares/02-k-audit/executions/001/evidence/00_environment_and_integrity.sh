#!/usr/bin/env bash
set -u

log=/audit-output/evidence/00_environment_and_integrity.log
exec > >(tee "$log") 2>&1

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

printf 'AUDIT_STAGE: 1 input and provenance integrity\n'
run test ! -e /reference/reference-semantics
run test ! -L /reference/reference-semantics
run find /reference -maxdepth 2 -printf '%y %p -> %l\n'
run find /candidate -maxdepth 1 -printf '%y %f %s -> %l\n'
run find /candidate/codex-trace -type f -printf '%y %p %s -> %l\n'
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /reference/canonical.py

required=(
  /candidate/run-input.json
  /candidate/metrics.json
  /candidate/codex-last.txt
  /candidate/codex-output.log
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/solution.py
  /candidate/solution.mpy
  /candidate/semantic.k
  /candidate/verification.k
  /candidate/spec.k
  /candidate/prove.sh
)
for artifact in "${required[@]}"; do
  run test -f "$artifact"
  run test ! -L "$artifact"
done

run command -v python3
run python3 --version
run command -v kompile
run kompile --version
run command -v krun
run krun --version
run command -v kprove
run kprove --version
