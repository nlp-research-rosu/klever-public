#!/usr/bin/env bash
set -u

record() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  command_status=$?
  printf 'EXIT_STATUS: %s\n' "$command_status"
  return "$command_status"
}

record sha256sum \
  /audit-campaign-lock.json \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T21-52-48-019f8ce3-d1dc-7f80-b54a-00f6e2d254c8.jsonl

record cmp -s /candidate/prompt.py /reference/prompt.py
record cmp -s /candidate/py2mpy.py /reference/py2mpy.py
record diff -r --no-dereference /candidate/reference-semantics /reference/reference-semantics

record find /candidate/reference-semantics -mindepth 1 -printf '%y %m %P -> %l\n'
record find /reference/reference-semantics -mindepth 1 -printf '%y %m %P -> %l\n'
record find /candidate /generation-evidence -type l -printf '%p -> %l\n'
