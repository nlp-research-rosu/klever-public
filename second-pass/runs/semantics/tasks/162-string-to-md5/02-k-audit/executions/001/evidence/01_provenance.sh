#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

required=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/runtime-metrics.json
  /generation-evidence/usage.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
)

run test -r /reference/reference-semantics
for path in "${required[@]}"; do
  run test -f "$path"
  run test -r "$path"
done
run test -d /generation-evidence/codex-trace
run test -r /generation-evidence/codex-trace
run find /generation-evidence/codex-trace -type f -print

run sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/runtime-metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

while IFS= read -r path; do
  run sha256sum "$path"
done < <(find /generation-evidence/codex-trace -type f -print | LC_ALL=C sort)

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics

run find /candidate/reference-semantics -type l -print
run find /reference/reference-semantics -type l -print
run find /candidate -maxdepth 1 -type l -print

run python3 -c 'import json; a=json.load(open("/audit-input.json")); b=json.load(open("/audit-campaign-lock.json")); assert a["audit_campaign"] == b; print("campaign blocks equal")'

run kompile --version
run kprove --version
