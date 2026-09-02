#!/usr/bin/env bash
set -u

run() {
  local cmd="$1"
  printf '$ %s\n' "$cmd"
  bash -o pipefail -c "$cmd"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run "pwd"
run "date --iso-8601=seconds"
run "stat -c '%F %N' /reference /reference/canonical.py /reference/prompt.py /reference/py2mpy.py /candidate"
run "test ! -e /reference/reference-semantics"
run "test ! -L /reference/reference-semantics"
run "test ! -e /candidate/reference-semantics"
run "command -v kompile"
run "command -v kprove"
run "command -v krun"
run "kompile --version"
run "kprove --version"
run "krun --version"
