#!/usr/bin/env bash
set +e

record() {
  printf '$ %s\n' "$*"
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return 0
}

if test -e /reference/reference-semantics || test -L /reference/reference-semantics; then
  printf 'GENERATED_SEMANTICS boundary: CONTRADICTION (reference semantics present)\n'
else
  printf 'GENERATED_SEMANTICS boundary: OK (reference semantics absent)\n'
fi

record find /reference -maxdepth 2 -printf '%y %p -> %l\n'
record find /candidate -path /candidate/semantic-kompiled -prune -o -maxdepth 8 -printf '%y %p -> %l\n'
record sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/spec.k /candidate/verification.k
record cmp /reference/prompt.py /candidate/prompt.py
record cmp /reference/py2mpy.py /candidate/py2mpy.py
record kompile --version
record kprove --version
record krun --version

for required in \
  run-input.json metrics.json codex-last.txt codex-output.log \
  prompt.py py2mpy.py solution.py solution.mpy semantic.k verification.k spec.k prove.sh
do
  if test -f "/candidate/$required" && ! test -L "/candidate/$required"; then
    printf 'REQUIRED REGULAR FILE: %s\n' "$required"
  else
    printf 'REQUIRED ARTIFACT PROBLEM: %s\n' "$required"
  fi
done

record find /candidate/codex-trace -type f -printf '%y %s %p -> %l\n'
