#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run python3 /audit-output/evidence/inspect_generation.py

required=(
  /audit-input.json
  /audit-campaign-lock.json
  /run.json
  /task.json
  /generation-result.json
  /generation-evidence/invocation.json
  /generation-evidence/metrics.json
  /generation-evidence/codex-last.txt
  /generation-evidence/codex-output.log
  /generation-evidence/prompt.txt
  /generation-evidence/usage.json
  /generation-evidence/codex-trace
  /reference/canonical.py
  /reference/prompt.py
  /reference/py2mpy.py
  /reference/reference-semantics
  /candidate
  /candidate/prompt.py
  /candidate/py2mpy.py
  /candidate/reference-semantics
)

for path in "${required[@]}"; do
  if [[ -r "$path" ]]; then
    printf 'READABLE %s\n' "$path"
  else
    printf 'MISSING_OR_UNREADABLE %s\n' "$path"
  fi
done

run sha256sum \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/usage.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

run sha256sum /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T23-54-55-019f8d53-a024-7c12-a582-699955cf5142.jsonl

run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics

run find /candidate/reference-semantics /reference/reference-semantics -type l -print
run find /candidate /reference /generation-evidence -xtype l -print

run bash -c 'cd /reference/reference-semantics && find . -printf "%y %P\n" | LC_ALL=C sort'
run bash -c 'cd /candidate/reference-semantics && find . -printf "%y %P\n" | LC_ALL=C sort'
run bash -c 'cd /reference/reference-semantics && find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum'
run bash -c 'cd /candidate/reference-semantics && find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum'

run find /generation-evidence/codex-trace -type f -printf '%P %s bytes\n'
run wc -l /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T23-54-55-019f8d53-a024-7c12-a582-699955cf5142.jsonl
run sed -n 1,220p /generation-evidence/prompt.txt
run sed -n 1,220p /generation-evidence/codex-last.txt
run tail -n 120 /generation-evidence/codex-output.log
