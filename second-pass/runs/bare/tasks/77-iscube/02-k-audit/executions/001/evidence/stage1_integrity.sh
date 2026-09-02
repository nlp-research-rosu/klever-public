#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf 'Audit mode: GENERATED_SEMANTICS\n'
run test '!' -e /reference/reference-semantics
run find /reference -maxdepth 2 -printf '%y %p -> %l\n'
run find /candidate -type l -printf '%p -> %l\n'

required=(
  run-input.json
  metrics.json
  codex-last.txt
  codex-output.log
  prompt.py
  py2mpy.py
  solution.py
  solution.mpy
  semantic.k
  spec.k
  verification.k
)

for artifact in "${required[@]}"; do
  run test -f "/candidate/$artifact"
  run test '!' -L "/candidate/$artifact"
  run stat -c '%F %s bytes %n' "/candidate/$artifact"
done

run find /candidate/codex-trace -type f -printf '%y %s bytes %p\n'
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum \
  /candidate/prompt.py /reference/prompt.py \
  /candidate/py2mpy.py /reference/py2mpy.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/spec.k /candidate/verification.k

run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json

printf '\nOptional candidate artifacts:\n'
for artifact in PROOF.md spec-vacuity.k; do
  if [[ -e "/candidate/$artifact" ]]; then
    run stat -c '%F %s bytes %n' "/candidate/$artifact"
  else
    printf '%s: absent\n' "$artifact"
  fi
done
