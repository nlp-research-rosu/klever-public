#!/usr/bin/env bash
set -u

TRACE=/candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-55-25-019f8977-4e3e-71c0-986d-d152bdd10050.jsonl
status=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local command_status=$?
  printf '[exit %d]\n' "$command_status"
  if (( command_status != 0 )); then
    status=1
  fi
}

printf '%s\n' 'Generated-semantics boundary'
if [[ -e /reference/reference-semantics || -L /reference/reference-semantics ]]; then
  printf '%s\n' 'BREACH: /reference/reference-semantics exists'
  status=1
else
  printf '%s\n' 'PASS: /reference/reference-semantics is absent'
fi

printf '\n%s\n' 'Candidate and trusted trees with entry types'
run find /candidate -xdev -printf '%y %m %s %p -> %l\n'
run find /reference -xdev -printf '%y %m %s %p -> %l\n'

printf '\n%s\n' 'Symlink scan'
run find /candidate -xdev -type l -printf '%p -> %l\n'
run find /reference -xdev -type l -printf '%p -> %l\n'

printf '\n%s\n' 'Trusted-input hashes and comparisons'
run sha256sum /candidate/prompt.py /reference/prompt.py
run cmp /candidate/prompt.py /reference/prompt.py
run sha256sum /candidate/py2mpy.py /reference/py2mpy.py
run cmp /candidate/py2mpy.py /reference/py2mpy.py

printf '\n%s\n' 'Required provenance JSON'
run python3 -m json.tool /candidate/run-input.json
run python3 -m json.tool /candidate/metrics.json

printf '\n%s\n' 'Complete structured-trace parse and bounded summary'
run python3 /audit-output/evidence/trace_summary.py "$TRACE"

printf '\n%s\n' 'Toolchain'
run /usr/bin/kompile --version
run /usr/bin/kprove --version

printf '\nfinal_status=%d\n' "$status"
exit "$status"
