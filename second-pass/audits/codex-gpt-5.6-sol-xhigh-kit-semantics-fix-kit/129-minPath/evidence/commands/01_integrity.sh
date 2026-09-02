#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
}

run test -d /reference/reference-semantics
run find /candidate -maxdepth 1 -printf '%y %f -> %l\n'
run find /reference -maxdepth 1 -printf '%y %f -> %l\n'
run find /candidate -type l -printf '%p -> %l\n'
run find /candidate/reference-semantics -printf '%P\t%y\t%l\n'
run find /reference/reference-semantics -printf '%P\t%y\t%l\n'
run diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum /reference/prompt.py /candidate/prompt.py /reference/py2mpy.py /candidate/py2mpy.py
run stat -c '%F %n' /candidate/run-input.json /candidate/metrics.json /candidate/codex-last.txt /candidate/codex-output.log /candidate/prompt.py /candidate/py2mpy.py /candidate/solution.py /candidate/solution.mpy /candidate/spec.k /candidate/verification.k
run find /candidate/codex-trace -type f -printf '%p\t%s bytes\n'
run kompile --version
run kprove --version
run krun --version
