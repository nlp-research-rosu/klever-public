#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

run sha256sum \
  /audit-input.json \
  /audit-campaign-lock.json \
  /run.json \
  /task.json \
  /generation-result.json \
  /generation-evidence/invocation.json \
  /generation-evidence/metrics.json \
  /generation-evidence/usage.json \
  /generation-evidence/codex-last.txt \
  /generation-evidence/codex-output.log \
  /generation-evidence/prompt.txt \
  /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T08-22-56-019f8f24-b7d4-73f3-8cab-481aed17f1e2.jsonl \
  /reference/canonical.py \
  /reference/prompt.py \
  /reference/py2mpy.py \
  /candidate/prompt.py \
  /candidate/py2mpy.py

run python3 -c 'import json; a=json.load(open("/audit-input.json")); b=json.load(open("/audit-campaign-lock.json")); assert a["audit_campaign"] == b'
run cmp -s /candidate/prompt.py /reference/prompt.py
run cmp -s /candidate/py2mpy.py /reference/py2mpy.py
run diff -qr --no-dereference /candidate/reference-semantics /reference/reference-semantics

run find /candidate /reference /generation-evidence -type l -printf '%p -> %l\n'
run find /candidate/reference-semantics -printf '%y %P\n'
run find /reference/reference-semantics -printf '%y %P\n'

run test -r /run.json
run test -r /task.json
run test -r /generation-result.json
run test -r /generation-evidence/invocation.json
run test -r /generation-evidence/metrics.json
run test -r /generation-evidence/codex-last.txt
run test -r /generation-evidence/codex-output.log
run test -r /generation-evidence/prompt.txt
run test -r /generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T08-22-56-019f8f24-b7d4-73f3-8cab-481aed17f1e2.jsonl
run test -r /generation-evidence/usage.json
run test -d /reference/reference-semantics
run test -d /candidate/reference-semantics

run env PATH="/home/agent/.nix-profile/bin:$PATH" kompile --version
run env PATH="/home/agent/.nix-profile/bin:$PATH" kprove --version
