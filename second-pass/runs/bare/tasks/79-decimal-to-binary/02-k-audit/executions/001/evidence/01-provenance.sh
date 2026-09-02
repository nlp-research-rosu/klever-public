#!/usr/bin/env bash
set -u

overall=0
run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

printf '%s\n' '$ test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics'
test ! -e /reference/reference-semantics && test ! -L /reference/reference-semantics
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

run find -H /candidate -maxdepth 4 -printf '%y %p -> %l\n'
run find -H /reference -maxdepth 3 -printf '%y %p -> %l\n'
run cmp /candidate/prompt.py /reference/prompt.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum \
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
  /candidate/prove.sh \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /reference/canonical.py
run python3 /audit-output/evidence/inspect_trace.py

printf '[script exit %d]\n' "$overall"
exit "$overall"
