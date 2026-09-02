#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

run test ! -e /reference/reference-semantics
run cmp -s /reference/prompt.py /candidate/prompt.py
run cmp -s /reference/py2mpy.py /candidate/py2mpy.py
run sha256sum \
  /reference/prompt.py /candidate/prompt.py \
  /reference/py2mpy.py /candidate/py2mpy.py \
  /reference/canonical.py \
  /candidate/solution.py /candidate/solution.mpy \
  /candidate/semantic.k /candidate/unicode-case.k \
  /candidate/verification.k /candidate/spec.k \
  /candidate/gen_unicode_case.py /candidate/prove.sh
run find /candidate -maxdepth 4 -printf '%y|%m|%s|%p|%l\n'
run find /candidate -type l -print
run find /reference -maxdepth 2 -printf '%y|%m|%s|%p|%l\n'
run stat -c '%F|%a|%s|%n' \
  /candidate/run-input.json /candidate/metrics.json \
  /candidate/codex-last.txt /candidate/codex-output.log
run command -v kompile
run kompile --version
run command -v kprove
run kprove --version
run command -v krun
run python3 --version
