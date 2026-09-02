#!/usr/bin/env bash
set -u

log="/audit-output/evidence/provenance.log"
exec >"$log" 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run date -u
run pwd
run kompile --version
run kprove --version
run ls -ld /reference /reference/reference-semantics /candidate
run find /reference -maxdepth 2 -printf '%y %p -> %l\n'
run find /candidate -maxdepth 6 -printf '%y %p -> %l\n'
run cmp -s /candidate/prompt.py /reference/prompt.py
run diff -u /reference/prompt.py /candidate/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -u /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum /reference/canonical.py /reference/prompt.py /reference/py2mpy.py
run sha256sum /candidate/prompt.py /candidate/py2mpy.py /candidate/solution.py /candidate/solution.mpy /candidate/semantic.k /candidate/spec.k /candidate/verification.k
run sed -n 1,240p /candidate/run-input.json
run sed -n 1,240p /candidate/metrics.json
run sed -n 1,320p /candidate/codex-last.txt
run sed -n 1,400p /candidate/codex-output.log
run find /candidate/codex-trace -type f -printf '%p\n'
