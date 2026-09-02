#!/usr/bin/env bash
set -u

run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  return "$status"
}

run python3 /audit-output/evidence/stage1_integrity.py
run python3 -m json.tool /run.json
run python3 -m json.tool /task.json
run python3 -m json.tool /generation-result.json
run python3 -m json.tool /generation-evidence/invocation.json
run python3 -m json.tool /generation-evidence/metrics.json
run python3 -m json.tool /generation-evidence/usage.json
run python3 -m json.tool /generation-evidence/legacy-metrics.json
run python3 -m json.tool /generation-evidence/legacy-run-input.json
run python3 /audit-output/evidence/trace_inspect.py
run sed -n 1,240p /generation-evidence/codex-last.txt
run sed -n 1,320p /generation-evidence/prompt.txt
run sha256sum \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt
