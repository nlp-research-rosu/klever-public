#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n\n' "$status"
}

printf 'MODE: SUPPLIED_SEMANTICS\n'
run test -d /reference/reference-semantics
run test -d /candidate/reference-semantics
run test -f /candidate/run-input.json
run test -f /candidate/metrics.json
run test -f /candidate/codex-last.txt
run test -f /candidate/codex-output.log
run test -f /candidate/solution.py
run test -f /candidate/solution.mpy
run test -f /candidate/spec.k
run test -f /candidate/verification.k
run test -f /candidate/prove.sh
run test -f /candidate/PROOF.md
run test -f /candidate/codex-trace/2026/07/23/rollout-2026-07-23T04-38-09-019f8e56-ef59-7241-ab33-f94739461da5.jsonl
run test ! -L /candidate/run-input.json
run test ! -L /candidate/metrics.json
run test ! -L /candidate/codex-last.txt
run test ! -L /candidate/codex-output.log
run test ! -L /candidate/prompt.py
run test ! -L /candidate/py2mpy.py
run test ! -L /candidate/solution.py
run test ! -L /candidate/solution.mpy
run test ! -L /candidate/spec.k
run test ! -L /candidate/verification.k
run test ! -L /candidate/prove.sh
run test ! -L /candidate/PROOF.md
run test ! -L /candidate/codex-trace/2026/07/23/rollout-2026-07-23T04-38-09-019f8e56-ef59-7241-ab33-f94739461da5.jsonl
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /reference/reference-semantics /candidate/reference-semantics
run find /candidate/reference-semantics -type l -print
run find /candidate/reference-semantics -type d -o -type f
run sha256sum /candidate/prompt.py /reference/prompt.py /candidate/py2mpy.py /reference/py2mpy.py
run sha256sum /candidate/solution.py /candidate/solution.mpy /candidate/spec.k /candidate/verification.k
