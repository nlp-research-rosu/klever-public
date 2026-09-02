#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return 0
}

run find /reference -maxdepth 3 -printf '%y %m %u:%g %s %p -> %l\n'
run find /candidate -printf '%y %m %u:%g %s %p -> %l\n'
run find /generation-evidence -printf '%y %m %u:%g %s %p -> %l\n'
run sha256sum /reference/canonical.py /reference/prompt.py /reference/py2mpy.py
run sha256sum /candidate/prompt.py /candidate/py2mpy.py
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run test ! -e /reference/reference-semantics
run sha256sum /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt
if [[ -e /generation-evidence/usage.json ]]; then
  run sha256sum /generation-evidence/usage.json
fi
run du -ah /candidate /generation-evidence
run sed -n 1,260p /run.json
run sed -n 1,260p /task.json
run sed -n 1,260p /generation-result.json
run sed -n 1,320p /generation-evidence/invocation.json
run sed -n 1,320p /generation-evidence/metrics.json
if [[ -e /generation-evidence/usage.json ]]; then
  run sed -n 1,320p /generation-evidence/usage.json
fi
run sed -n 1,320p /generation-evidence/prompt.txt
run sed -n 1,320p /generation-evidence/codex-last.txt
run sed -n 1,640p /generation-evidence/codex-output.log
run find /generation-evidence/codex-trace -type f -print0
